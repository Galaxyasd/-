from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# 指定本地保存的路径
local_model_path = "./chinese-roberta-wwm-ext"  # 你的文件夹路径

# 加载Tokenzier和模型
tokenizer = AutoTokenizer.from_pretrained(local_model_path)
model = AutoModelForSequenceClassification.from_pretrained(local_model_path)

# 创建zero-shot分类pipeline
classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)

sequence_to_classify = """
最近，小李决定尝试一种新的生活方式——每天早晨起床后，他都会花一个小时在公园里散步。这不仅让他感受到了大自然的美丽，还让他整天都保持着充沛的精力。走在林荫小道上，他能够闻到树木的清香，听到鸟儿的歌唱，这让他觉得整个人都放松了下来。

散步结束后，小李会在公园旁边的一家咖啡馆停留片刻，点上一杯黑咖啡，坐在窗边静静地阅读一本书。这是他一天中最享受的时光，他认为这不仅仅是喝咖啡，而是一种心灵的休息。

随着时间的推移，小李发现他的身体状况明显改善了，他的心情也变得更加愉悦。这样的生活方式让他感到非常满足，他决定将这种习惯坚持下去。
"""

candidate_labels = ["健康生活", "早晨习惯", "自然景观", "公园散步", "咖啡文化", "健身", "读书", "放松", "心灵休息", "幸福感", "时间管理", "生活方式"]


result = classifier(sequence_to_classify, candidate_labels)

print(result)