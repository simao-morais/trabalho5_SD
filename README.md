# Trabalho 5 - Tolerância a Falhas e Monitoramento com Kubernetes

## 📋 Descrição do Projeto

Aplicação distribuída de conversão de vídeo para áudio (MP3) implantada em cluster Kubernetes com mecanismos de tolerância a falhas, auto-recuperação e escalonamento horizontal automático.

## 🎯 Objetivo

Demonstrar técnicas de alta disponibilidade em ambientes containerizados usando:
- **Auto-healing**: Recriação automática de pods em caso de falha
- **Horizontal Pod Autoscaler (HPA)**: Escalonamento baseado em uso de CPU
- **Monitoramento**: Prometheus para métricas em tempo real

---

## 🖥️ Notebook A - Cluster Kubernetes

### Arquitetura da Aplicação

```
conversor-video-app/
├── app.py                 # Aplicação Flask
├── requirements.txt       # Dependências Python
├── Dockerfile            # Imagem Docker
├── templates/
│   └── index.html        # Interface web
└── kubernetes/
    ├── deployment.yaml   # Deployment com 2 réplicas
    ├── service.yaml      # Service NodePort
    └── hpa.yaml          # HPA configurado
```

### Tecnologias Utilizadas

- **Python 3.9** + Flask
- **MoviePy** para conversão de vídeo
- **Docker** para containerização
- **Kubernetes (Minikube)** para orquestração
- **Metrics Server** para coleta de métricas

---

## 🚀 Instalação e Configuração

### Pré-requisitos

- Docker Desktop instalado e em execução
- Minikube instalado
- kubectl configurado
- Python 3.9+ (para desenvolvimento local)

### 1️⃣ Iniciar o Cluster Kubernetes

```bash
# Iniciar Minikube
minikube start

# Verificar status
minikube status

# Habilitar o Metrics Server (necessário para HPA)
minikube addons enable metrics-server

# Aguardar metrics-server inicializar (30-60 segundos)
kubectl get pods -n kube-system | Select-String metrics-server  # powershell
ou
kubectl get pods -n kube-system | grep metrics-server
```

### 2️⃣ Construir a Imagem Docker

```bash
# Navegar até a pasta da aplicação
cd aplicacao/

# Build da imagem
docker build -t simaomorais/conversor-video:1.0 .

# Carregar imagem no Minikube
minikube image load simaomorais/conversor-video:1.0

# Verificar se a imagem foi carregada
minikube ssh
docker images | grep conversor-video
exit
```

### 3️⃣ Implantar a Aplicação no Kubernetes

```bash
# Voltar para a pasta raiz do projeto
cd ..

# Aplicar os manifests
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml

# Verificar deployment
kubectl get deployments
kubectl get pods
kubectl get hpa
kubectl get services
```

### 4️⃣ Acessar a Aplicação

```bash
# Obter URL do serviço
minikube service conversor-video-service --url

# Ou abrir diretamente no navegador
minikube service conversor-video-service
```

A aplicação estará disponível em `http://<NODE-IP>:30007`

---

## 🔧 Configurações Kubernetes

### Deployment

- **Réplicas iniciais**: 2
- **CPU Request**: 100m
- **CPU Limit**: 200m
- **Porta**: 5000
- **Imagem**: simaomorais/conversor-video:1.0

### Service

- **Tipo**: NodePort
- **Porta do Service**: 5000
- **NodePort**: 30007

### Horizontal Pod Autoscaler (HPA)

- **Métrica**: CPU Utilization
- **Target**: 50% de uso médio
- **Min Replicas**: 2
- **Max Replicas**: 5

---

## 🧪 Testes de Tolerância a Falhas

### Teste 1: Auto-Healing (Deleção Manual de Pod)

**Objetivo**: Verificar recriação automática de pods

```bash
# 1. Verificar estado inicial
kubectl get pods -o wide

# 2. Deletar um pod manualmente
kubectl delete pod <NOME-DO-POD>

# 3. Monitorar recriação (em outro terminal)
kubectl get pods -w
```

**Comportamento esperado**:
- Pod deletado entra em estado `Terminating`
- Kubernetes detecta a falta de réplicas
- Novo pod é criado automaticamente
- Sistema volta a ter 2 réplicas em `Running`

### Teste 2: Escalonamento Horizontal (Sobrecarga de CPU)

**Objetivo**: Verificar escalonamento automático baseado em CPU

#### Monitoramento (abrir em terminais separados):

```bash
# Terminal 1: Monitorar HPA
kubectl get hpa conversor-video-hpa -w

# Terminal 2: Monitorar pods
kubectl get pods -w

# Terminal 3: Monitorar uso de CPU
kubectl top pods

# Terminal 4: Verificar métricas detalhadas
while true; do clear; kubectl top pods; sleep 2; done  #GitBash
```

#### Gerar Carga de CPU:

```bash
# Pegar nome de um pod
kubectl get pods

# Executar stress de CPU no pod
kubectl exec -it <NOME-DO-POD> -- python3 -c "while True: pass"

# Para parar: Ctrl+C
```

**Comportamento esperado**:
1. CPU do pod sobe acima de 50%
2. HPA detecta a sobrecarga
3. Novos pods são criados (até 5 réplicas)
4. Carga é distribuída entre os pods
5. Após parar o stress, HPA reduz réplicas gradualmente

---

## 📊 Comandos Úteis de Monitoramento

```bash
# Status geral do cluster
kubectl get all

# Detalhes de um pod específico
kubectl describe pod <NOME-DO-POD>

# Logs de um pod
kubectl logs <NOME-DO-POD>

# Logs em tempo real
kubectl logs -f <NOME-DO-POD>

# Uso de recursos
kubectl top nodes
kubectl top pods

# Status do HPA
kubectl get hpa
kubectl describe hpa conversor-video-hpa

# Eventos do cluster
kubectl get events --sort-by=.metadata.creationTimestamp

# Acessar terminal de um pod
kubectl exec -it <NOME-DO-POD> -- /bin/bash
```

---

## 🐛 Troubleshooting

### Pods em CrashLoopBackOff

```bash
# Ver logs do pod
kubectl logs <NOME-DO-POD>

# Ver eventos
kubectl describe pod <NOME-DO-POD>

# Verificar se a imagem foi carregada
minikube ssh
docker images
```

### HPA mostrando <unknown>

```bash
# Verificar metrics-server
kubectl get pods -n kube-system | grep metrics

# Reiniciar metrics-server se necessário
minikube addons disable metrics-server
minikube addons enable metrics-server

# Aguardar 1-2 minutos para coleta de métricas
```

### Aplicação não acessível

```bash
# Verificar service
kubectl get svc

# Verificar porta do NodePort
kubectl describe svc conversor-video-service

# Obter IP do Minikube
minikube ip

# Acessar: http://<MINIKUBE-IP>:30007
```

---

## 🧹 Limpeza do Ambiente

```bash
# Deletar recursos da aplicação
kubectl delete -f hpa.yaml
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml

# Ou deletar tudo de uma vez
kubectl delete all -l app=conversor-video

# Parar Minikube
minikube stop

# Deletar cluster (opcional)
minikube delete
```

---

## 📝 Estrutura de Arquivos Kubernetes

### deployment.yaml
Define o Deployment com 2 réplicas, limites de recursos e seletor de labels.

### service.yaml
Expõe a aplicação via NodePort na porta 30007.

### hpa.yaml
Configura escalonamento automático baseado em CPU (50% target, 2-5 réplicas).

---

## 👥 Autor

Trabalho desenvolvido para a disciplina de Sistemas Distribuídos.

## 📄 Licença

Este projeto é parte de um trabalho acadêmico.