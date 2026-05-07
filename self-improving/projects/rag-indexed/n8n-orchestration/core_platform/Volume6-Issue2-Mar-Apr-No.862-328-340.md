---
source_block: core_platform
source_file: Volume6-Issue2-Mar-Apr-No.862-328-340.pdf
topic_tags: ["n8n", "core platform"]
---

# Volume6-Issue2-Mar-Apr-No.862-328-340

International Journal of Scientific Advances
ISSN: 2708-7972
Volume: 6 | Issue: 2 | Mar – Apr 2025 Available Online: www.ijscia.com
DOI: 10.51542/ijscia.v6i2.15
Building AI-Driven Cloud-Na tive Applications
with Kubernetes and Containerization
Prudhvi Naayini
Independent Researcher
Corresponding author: naayini.prudhvi@gmail.com
ABSTRACT
Modern enterprises increasingly deploy AI-driven services in cloud environments, demanding scalable
infrastructure that aligns machine learning operations (MLOps) with cloud-native principles. This paper
proposes a Kubernetes-based architecture for developing and deploying AI applications, emphasizing
containerization, orchestration, and continuous delivery. The architecture supports end-to-end MLOps
workflows from training and versioning to real-time inference and monitoring using open-source tools on
managed Kubernetes services (e.g., Amazon EKS, Azure AKS, Google GKE). Core components include Kubeflow
Pipelines for orchestration, Ml flow for model registry, Argo Workflows for automation, and serving frameworks
such as TensorFlow Serving and ONNX Runtime for scalable inference. Cloud-native features like autoscaling,
service mesh, observability, and security are integrated using tools such as Prometheus, Grafana, Trivy, and Vault.
The architecture is validated through two use cases: an e-commerce recommendation service and an IoT
anomaly detection pipeline, with a proof-of-concept deployed on AWS. Experimental results demonstrate low-
latency inference (95th percentile latency under 120, ms at 100 requests/s) and efficient resource utilization.
The platform enhances reproducibility, monitoring, and deployment speed over traditional ML deployment
approaches. These findings highlight the advantages of Kubernetes-native MLOps for scalable, reliable AI systems
in production environments.
Keywords: Cloud Computing; Kubernetes; MLOps; Machine Learning; Deep Learning; DevOps; Containerization;
Autoscaling; Microservices; IoT; E-commerce.
I. INTRODUCTION cloud providers offer managed Kuber- notes services
Artificial intelligence (AI) and machine learning are (Amazon EKS, Azure AKS, Google GKE) that abstract
being deployed across nearly every industry, from away control plane management and improve
personalized recommendations in e-commerce to real- reliability; for example, Amazon EKS manages the
time analytics in Internet of Things (IoT) scenarios. As Kubernetes control plane across availability zones for
organizations incorporate predictive models into high availability and automates node provisioning.
production services (e.g., sales forecasting, anomaly
detection), they face the challenge of maintaining and Despite the availability of cloud-specific ML platforms
scaling these models with the same rigor as traditional (e.g., AWS SageMaker, Azure ML), these proprietary
software microservices. This convergence of AI solutions often operate as black boxes with limited
development and robust operations has led to the flexibility. In contrast, an open, cloud-agnostic MLOps
emergence of Machine Learning Operations (MLOps) – architecture built on Kubernetes can provide
a set of practices to reliably deploy and manage ML modularity, transparency, and control over the entire
models in production. ML lifecycle. Prior works have proposed various
components of such an open architecture: for
Kubernetes has rapidly become a cornerstone of instance, Fursin et al. introduced CodeReef, an open
cloud-native computing and is increasingly the platform for portable MLOps emphasizing
platform of choice for MLOps deployment. Originally reproducible model deployment and benchmarking;
open-sourced by Google, Kubernetes automates One Click Deep Learning (OCDL) provides tools for
container scheduling, scaling, and management, and encapsulation, resource sharing, and model
is now adopted by over half of organizations versioning. Alibaba’s LinkEdge project extends
worldwide [1]. Its inherent features – self-healing, MLOps to IoT edge devices, automating data
horizontal scaling, load balancing, and declarative collection, training, and deployment in distributed
deployments provide an ideal substrate for AI environments. However, these solutions address
microservices. By containerizing portions of the pipeline and often lack integration or
ease of use. There remains a need for a unified
ML workloads and orchestrating them on framework that combines best-of-breed open-source
Kubernetes, teams can achieve reproducibility and tools into a cohesive pipeline, leveraging Kubernetes
scalability in model training and inference. Major to orchestrate end-to-end workflows.
Available Online at www.ijscia.com | Volume 6 | Issue 2 | Mar – Apr 2025 328
International Journal of Scientific Advances ISSN: 2708-7972
A. Purpose and Scope Section III details the proposed architecture,
In this work, we present a full-stack approach to describing each component and its role in the end-to-
building AI-driven cloud-native applicati
