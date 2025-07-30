# **Endura SDK**

The **Endura SDK** provides a trust layer for edge AI models, allowing you to securely log telemetry, capture model metadata, and validate data at the edge.

---

## **Usage**

### **Using the SDK in Python**:

Once the SDK is installed, you can import and use it in your Python code:

```python
from endura import EnduraAgent

# Initialize with your model path
agent = EnduraAgent("path_to_model.pth")

# Log an inference event
agent.log_inference(input_data, output_data)
```