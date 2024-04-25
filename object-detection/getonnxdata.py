import onnx

onnx_model = onnx.load('/models/yolov8n.onnx')

for input in onnx_model.graph.input:
    print(input.name)

for output in onnx_model.graph.output:
    print(output.name)