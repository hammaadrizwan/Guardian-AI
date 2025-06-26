
# Guardian.ai 🔒

Welcome to **Guardian.ai**, our AI-driven surveillance system designed to improve public safety by detecting firearms and unattended baggage in real time using cutting-edge Artificial Intelligence techniques.

## 📌 Overview

In light of rising threats to public safety, especially in places like railway stations and bus depots, **Guardian.ai** aims to provide fast and reliable threat detection. By leveraging object detection and fine-grained image classification, this platform delivers real-time analysis and alerts, minimizing response times and reducing false positives.


## 🛑 Problem Identification

Public safety in open spaces has become a growing concern due to:

- Increased number of threats in recent years (e.g., Easter Sunday attacks in Sri Lanka).
- Slow response times from traditional surveillance systems.
- Lack of effective utilization of video footage for model training and prediction improvement.
- Absence of integrated systems that detect both weapons and unattended baggage.
- Need for reducing false alarms and improving detection reliability.

## 🎯 Project Aim

**Guardian.ai** is an **Edge AI-based surveillance platform** that:

- Uses real-time CCTV image feeds to detect firearms and unattended baggage.
- Prioritizes **high accuracy** and **low latency** for real-time performance.
- Reduces false positives by identifying military personnel before raising an alert.
- Lays the foundation for scalable deployment across multiple public spaces.

## 🛠️ System Design

### Architecture Flow:

- **Hardware**: Raspberry Pi 5 with connected webcam (Edge Device).
- **Detection Pipeline**:
  1. Live video feed captured.
  2. **YOLO models** deployed on the edge device detect firearms or unattended baggage.
  3. On positive detection:
      - **CNN classifier** checks for military personnel.
      - If **non-military**, event details (time, date, and image frame) are saved in **Amazon S3 buckets**.
      - Alert triggered on-site and sent via **email notification**.
- **Frontend**: Developed with **React.js** and **Tailwind CSS**, hosted on **AWS EC2**.
- **Scalability Plan**: Future deployment and training on **Amazon SageMaker** (pending compute resource availability).

## 📊 Model Evaluation

| Model                       | Architecture        | mAP50-95 (Train) | mAP50-95 (Test/Validation) |
|-----------------------------|---------------------|------------------|---------------------------|
| **Weapon Detection 1**       | YOLO 11m (Ultralytics) | 0.786          | 0.641                     |
| **Bag Detection**           | YOLO 11s            | 0.960            | 0.871                     |
| **Weapon Detection 2**       | YOLOv8s             | 0.817            | 0.711                     |
| **Military Personnel Detection** | Custom CNN + Fine-Grained Classification | 98.01% (Train Accuracy) | 92.21% (Test Accuracy) |

> Focus was given to optimizing **accuracy vs latency trade-off**, favoring smaller YOLO models to ensure higher FPS rates for real-time surveillance.

## 🚧 Challenges Faced

1. **Limited Computational Resources**: 
   - Could not train large YOLO models directly on Raspberry Pi 5.
   - Depended on smaller architectures like YOLOs and YOLOm.

2. **Dataset Limitations**: 
   - Lack of CCTV-quality images.
   - Required aggressive **image augmentation** to bridge quality mismatch.

3. **Latency vs Accuracy Trade-off**: 
   - Larger models decreased FPS, risking surveillance blind spots.
   - Aim to integrate **Google Coral USB Accelerator** in the future for better inference speed.

## 🔁 Changes from Initial Design

| Change | Reason |
|------|-------|
| Switched from **police call alerts** to **email alerts** | To facilitate MVP demonstration and reduce external dependencies. |
| **Military personnel classifier** added | To reduce false positives (by excluding military personnel from alerts). |
| Frontend hosted on **AWS EC2** | To leverage cloud scalability and reliability. |

> Future plans include integration with **Amazon SNS** for mobile phone alerts and **Amazon SageMaker** for model retraining on misclassified cases.

## ✅ Conclusion

**Guardian.ai** stands as a scalable, AI-powered surveillance solution built to address modern security challenges in public spaces. Though currently a Minimum Viable Product (MVP), its design is extensible for large-scale deployments with better hardware and resources.

Thank you for your interest in **Project Arkhash**. Together, let's make public spaces safer. 🛡️
### To start backend:

- cd backend
- pip install -r requirements.txt
- cd src
- python main.py

### To start frontend:

- cd frontend/guardian-ai
- npm install
- npm run dev
