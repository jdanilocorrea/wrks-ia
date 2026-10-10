import subprocess
import json

def check_squad_status() -> str:
    """Verifica o estado dos serviços systemd do Esquadrão de IA local."""
    services = ["ollama", "open-webui", "tts", "voicereader"]
    results = {}
    for svc in services:
        try:
            process = subprocess.run(["systemctl", "--user", "is-active", svc], capture_output=True, text=True)
            status = process.stdout.strip()
            results[svc] = status if status else "unknown"
        except Exception as e:
            results[svc] = f"error: {str(e)}"
    return json.dumps(results, indent=2)

def restart_failed_service(service_name: str) -> str:
    """Tenta reiniciar um serviço do Esquadrão de IA."""
    valid_services = ["ollama", "open-webui", "tts", "voicereader"]
    if service_name not in valid_services:
        return f"Erro: O serviço '{service_name}' não pertence ao Esquadrão de IA."
    try:
        subprocess.run(["systemctl", "--user", "restart", service_name], check=True)
        return f"Ordem de reinício enviada com sucesso para {service_name}."
    except subprocess.CalledProcessError as e:
        return f"Falha ao reiniciar {service_name}: {e}"

def get_service_logs(service_name: str, lines: int = 30) -> str:
    """Recupera as últimas linhas de log de um serviço para diagnóstico."""
    valid_services = ["ollama", "open-webui", "tts", "voicereader"]
    if service_name not in valid_services:
        return f"Erro: Serviço inválido."
    try:
        process = subprocess.run(
            ["journalctl", "--user", "-u", f"{service_name}.service", "-n", str(lines), "--no-pager"],
            capture_output=True, text=True, check=True
        )
        return process.stdout if process.stdout else "Sem logs disponíveis."
    except subprocess.CalledProcessError as e:
        return f"Falha ao ler os logs: {e}"
