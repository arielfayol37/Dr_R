from django.core.management.base import BaseCommand
import torch
from transformers import BertTokenizer, BertModel
from phobos.models import Question
from phobos.views import attention_pooling

class Command(BaseCommand):
    help = 'Create question embeddings'

    def handle(self, *args, **options):
        # Load pre-trained BERT model and tokenizer
        BERT_MODEL_NAME = 'bert-base-uncased'
        bert_tokenizer = BertTokenizer.from_pretrained(BERT_MODEL_NAME)
        bert_model = BertModel.from_pretrained(BERT_MODEL_NAME)
        bert_model.eval()

        # Loop through all questions and encode them
        for question in Question.objects.all():
            question_tokens = bert_tokenizer.encode(question.text, add_special_tokens=True)
            with torch.no_grad():
                question_tensor = torch.tensor([question_tokens])
                question_attention_mask = (question_tensor != 0).float()  # Create attention mask
                question_encoded_output = bert_model(question_tensor, attention_mask=question_attention_mask)[0]

            # Apply attention-based pooling to question encoded output
            question_encoded_output_pooled = attention_pooling(question_encoded_output, question_attention_mask)

            # Save the encoded output to the question object
            question.embedding = question_encoded_output_pooled.tolist()
            question.save()

        self.stdout.write(self.style.SUCCESS('Successfully created question embeddings'))
