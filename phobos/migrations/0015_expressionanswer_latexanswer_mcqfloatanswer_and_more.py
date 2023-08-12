# Generated by Django 4.2.3 on 2023-08-08 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('phobos', '0014_alter_mcqexpressionanswer_content_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpressionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='LatexAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='MCQFloatAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.FloatField()),
                ('is_answer', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MCQImageAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='phobos/images/question_images/')),
                ('is_answer', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MCQLatexAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=400)),
                ('is_answer', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='mcqexpressionanswer',
            name='is_answer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='answer_type',
            field=models.CharField(choices=[('STRUCTURAL_EXPRESSION', 'Structural Expression'), ('STRUCTURAL_FLOAT', 'Structural Float'), ('STRUCTURAL_TEXT', 'Structural Text'), ('STRUCTURAL_LATEX', 'Structural Latex'), ('MCQ_EXPRESSION', 'MCQ Expression'), ('MCQ_FLOAT', 'MCQ Float'), ('MCQ_LATEX', 'MCQ Latex'), ('MCQ_TEXT', 'MCQ Text')], default='STRUCTURAL_TEXT', max_length=30),
        ),
        migrations.AlterField(
            model_name='mcqexpressionanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mcq_expression_answers', to='phobos.question'),
        ),
        migrations.DeleteModel(
            name='McqAnswer',
        ),
        migrations.AddField(
            model_name='mcqlatexanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mcq_latex_answers', to='phobos.question'),
        ),
        migrations.AddField(
            model_name='mcqimageanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mcq_image_answers', to='phobos.question'),
        ),
        migrations.AddField(
            model_name='mcqfloatanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mcq_float_answers', to='phobos.question'),
        ),
        migrations.AddField(
            model_name='latexanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='latex_answers', to='phobos.question'),
        ),
        migrations.AddField(
            model_name='expressionanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expression_answers', to='phobos.question'),
        ),
    ]
