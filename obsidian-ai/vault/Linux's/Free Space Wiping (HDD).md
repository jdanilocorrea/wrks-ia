
O processo de saturação de espaço livre (Free Space Wiping) em discos magnéticos (HDDs) é crítico para garantir que arquivos previamente excluídos não possam ser recuperados por ferramentas de análise forense, ao mesmo tempo em que os arquivos atuais do disco são preservados. O script a seguir cria um arquivo massivo preenchido com zeros, saturando o espaço livre e forçando a sobrescrita mecânica dos setores.

Você pode copiar a estrutura abaixo diretamente para o seu Obsidian.

### 📘 Documentação: Free Space Wiping Seguro em HDDs Externos (Linux)

**Objetivo:** Eliminar definitivamente qualquer traço magnético de arquivos excluídos em um disco rígido tradicional (HDD), preservando os dados existentes. **Hardware Alvo:** HDDs externos mecânicos (ex: Samsung M3 Portable 1TB - `/dev/sdb`). **Arquitetura:** Injeção de E/S contígua via `dd` no espaço não alocado do sistema de arquivos.

#### ⚠️ Avisos Importantes

- **Tempo de Execução:** Em um HDD via USB 3.0 (aprox. 100 MB/s), o processo leva entre 1.5 a 2 horas para cada 500GB de espaço livre.
    
- **Controle Térmico:** A agulha gravará dados de forma contínua no limite da controladora. Mantenha o HDD em superfície dissipadora.
    
- **Não utilize em SSDs/NVMe:** Esta técnica causa desgaste desnecessário em memórias Flash. Para SSDs, o padrão é utilizar `fstrim`.
    

#### Procedimento Passo a Passo

O processo consiste em criar um arquivo temporário gigante, preencher o espaço livre do disco com dados nulos, forçar a gravação física (sync) e, em seguida, excluir o arquivo para liberar o espaço (agora purgado).

**1. Identificação do Dispositivo** Primeiro, localize o ponto de montagem exato do disco.

Bash

```
lsblk -f
```

_Localize a partição correta (ex: `sdb1`) e anote o caminho sob a coluna `MOUNTPOINTS` (geralmente `/run/media/$USER/NOME_DO_DISCO`)._

**2. Navegação e Preparação** Acesse o diretório raiz do disco montado:

Bash

```
cd /run/media/$USER/NOME_DO_DISCO
```

Crie o arquivo que será o recipiente da obliteração:

Bash

```
touch .shred_space.tmp
```

**3. Bypass de BTRFS (Opcional, apenas se o disco for BTRFS)** Se o seu HDD externo foi formatado em BTRFS (pouco provável para discos portáteis, mas essencial caso seja), você _precisa_ desabilitar o Copy-on-Write e a compressão para este arquivo, senão a operação falhará miseravelmente na camada lógica.

Bash

```
# Se o disco for NTFS ou exFAT, este comando retornará erro. Apenas ignore e prossiga.
chattr +C .shred_space.tmp 2>/dev/null
```

**4. Execução do Wiping (I/O Massivo)** Este comando satura o disco escrevendo blocos de 16MB de zeros. O uso de `/dev/zero` é otimizado para o limite máximo de velocidade de gravação em discos NTFS/exFAT.

_Se o disco for BTRFS com compressão ativa globalmente, altere `/dev/zero` para `/dev/urandom` para garantir que o algoritmo não comprima os dados, forçando a gravação física._

Bash

```
dd if=/dev/zero of=.shred_space.tmp bs=16M status=progress
```

**Ação requerida:** Aguarde. O comando rodará por horas e **terminará com o erro "No space left on device"**. Isso é o comportamento esperado e confirma que 100% do espaço livre foi sobrescrito.

**5. Sincronização e Finalização** Após o disco acusar que está cheio, force o kernel Linux a descarregar qualquer cache de RAM pendente diretamente para os pratos magnéticos.

Bash

```
sync
```

Delete o arquivo gigante. Isso devolverá imediatamente todo o seu espaço livre. O espaço devolvido não conterá mais nenhum dado recuperável.

Bash

```
rm -f .shred_space.tmp
```

Sincronize a tabela do sistema de arquivos uma última vez para garantir que a transação de remoção foi confirmada na controladora USB.

Bash

```
sync
```

#### Notas de Arquitetura

A escolha do comando `dd` com `bs=16M` (Block Size) evita overhead do processador e otimiza o fluxo contíguo na controladora USB e no cache DRAM nativo de HDDs (geralmente de 8MB a 32MB), maximizando a taxa de transferência contínua em relação a ferramentas de terceiros em linguagens de alto nível.


---


Bash

```
# 1. Identifique o ponto de montagem exato da partição sdb1
lsblk -f /dev/sdb1

# 2. Navegue até a raiz do disco montado (substitua pelo caminho real retornado acima)
cd /run/media/$USER/NOME_DO_DISCO

# 3. Verifique se é BTRFS. Se for, desative o CoW (se for NTFS/exFAT/EXT4, isso vai falhar, siga adiante sem problemas)
touch .shred_space.tmp
chattr +C .shred_space.tmp 2>/dev/null

# 4. Início do I/O Massivo.
# Otimização: Se o disco for NTFS/exFAT (sem compressão nativa), usar /dev/zero 
# é mais eficiente e garante o limite máximo de velocidade de escrita magnética da controladora USB.
# Se for BTRFS, mantenha /dev/urandom para driblar a compressão.
dd if=/dev/zero of=.shred_space.tmp bs=16M status=progress

# Aguarde até que o terminal retorne "No space left on device" (Sem espaço disponível no dispositivo).
# Isso garante que a agulha varreu todos os setores não mapeados até o final do prato.

# 5. Esvazie os buffers de gravação do kernel para garantir que a controladora USB terminou os blocos
sync

# 6. Delete o arquivo, recuperando instantaneamente todo o seu espaço livre
rm -f .shred_space.tmp

# 7. Sincronização final
sync
```




### Diagnóstico de Falha

Dois problemas estão ocorrendo na sua sessão:

1. **Interceptação do Shell:** Você tem o `zoxide` configurado como _alias_ do `cd`. O `zoxide` tentou buscar o caminho no banco de dados dele em vez de forçar a navegação absoluta, ou o `$USER` não foi expandido corretamente.
    
2. **Estado de Montagem (Lazy Mount):** No GNOME, o daemon `udisks2` reconhece o disco (como vimos no `lsblk`), mas **não o monta fisicamente** em `/run/media/...` até que você clique nele no gerenciador de arquivos (Nautilus) ou force a montagem via terminal.
    

### Solução Arquitetural

Vamos forçar a montagem diretamente pelo daemon de discos do Linux e usar o binário nativo de navegação, ignorando o `zoxide`.

Execute no Ptyxis:

Bash

```
# 1. Force a montagem da partição em user-space (sem precisar de sudo)
udisksctl mount -b /dev/sdb1

# O terminal deve retornar algo como: 
# "Mounted /dev/sdb1 at /run/media/SEU_USUARIO/elements1.0"

# 2. Use o comando 'command' para evadir o zoxide e invocar o 'cd' built-in do seu shell.
# Substitua SEU_USUARIO pelo seu nome de usuário real no sistema caso o $USER falhe novamente.
command cd /run/media/$USER/elements1.0

# 3. Confirme que você está no disco correto listando os arquivos atuais
ls -la
```

Se o `ls` mostrar os arquivos que você quer manter intactos, você está no diretório correto. Pode iniciar o I/O massivo:

Bash

```
dd if=/dev/zero of=.shred_space.tmp bs=16M status=progress
```