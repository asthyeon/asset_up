import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('nickname', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(choices=[('M', '남자'), ('F', '여자')], max_length=1)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('address', models.TextField(blank=True, help_text="예: '서울특별시 마포구 연남동 사파리월드 12-3'")),
                ('salary', models.IntegerField(blank=True, null=True)),
                ('money', models.IntegerField(blank=True, null=True)),
                ('target_asset', models.IntegerField(blank=True, null=True)),
                ('financial_products', models.TextField(blank=True, default='', null=True)),
                ('saving_type', models.CharField(blank=True, choices=[('thrifty', '알뜰형'), ('challenging', '도전형'), ('diligent', '성실형')], max_length=20, null=True)),
                ('favorite_company', models.CharField(blank=True, max_length=255, null=True)),
                ('mbti', models.CharField(blank=True, max_length=4, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
