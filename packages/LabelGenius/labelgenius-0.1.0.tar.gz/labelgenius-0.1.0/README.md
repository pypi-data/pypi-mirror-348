
# LabelGenius

LabelGenius is a Python package designed for zero-shot and fine-tuned classification tasks using CLIP and GPT models. It offers seamless integration with OpenAI models for text and image-based classification, fine-tuning, and price estimation.

---

## Installation

You can install LabelGenius from PyPI:

```bash
pip install LabelGenius
```

To install locally from source:

```bash
git clone https://github.com/yourusername/LabelGenius.git
cd LabelGenius
pip install -e .
```

---

## Modules & Functions

### 1. CLIP-based Classification

- `classification_CLIP_0_shot`: Perform zero-shot classification using CLIP.
- `classification_CLIP_finetuned`: Use a fine-tuned CLIP model for classification.
- `finetune_CLIP`: Fine-tune the CLIP model on your dataset.

### 2. GPT-based Classification

- `classification_GPT`: Perform text-based classification using GPT models.
- `generate_GPT_finetune_jsonl`: Prepare JSONL files for fine-tuning GPT models.
- `finetune_GPT`: Fine-tune a GPT model on your labeled data.

### 3. Auto Verification

- `auto_verification`: Automatically validate model predictions against ground truth labels.

### 4. Utility Functions

- `price_estimation`: Estimate the cost of API calls based on prompt and completion tokens.

---

## Usage Examples

### Zero-Shot Classification with CLIP

```python
from labelgenius import classification_CLIP_0_shot

df = classification_CLIP_0_shot(
    text_path='data/text_data.csv',
    img_dir='data/images/',
    mode='both',
    prompt=['Politics', 'Sports', 'Technology'],
    text_column=['headline'],
    predict_column='label'
)
print(df.head())
```

### Fine-Tune CLIP Model

```python
from labelgenius import finetune_CLIP

best_acc = finetune_CLIP(
    mode='both',
    text_path='data/train_data.csv',
    img_dir='data/images',
    text_column=['headline'],
    true_label='section_numeric',
    model_name='best_clip_model.pth',
    num_epochs=5
)
print(f'Best validation accuracy: {best_acc}')
```

### Fine-Tune GPT Model

```python
from labelgenius import finetune_GPT

finetune_GPT(
    training_file_path='data/gpt_training.jsonl',
    model='gpt-4o-mini',
    method_type='supervised'
)
```

---

## Contributing

We welcome contributions to LabelGenius! Feel free to submit issues or pull requests to improve the codebase.

---

## License

LabelGenius is released under the MIT License.
