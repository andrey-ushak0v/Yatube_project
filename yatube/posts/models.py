from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        default=None,
        help_text='Введите название',
        verbose_name='название группы'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        default=None,
        help_text='Введите слаг',
        verbose_name='слаг'
    )
    description = models.TextField(
        default=None,
        help_text='опишите группу',
        verbose_name='описание'
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        max_length=400,
        help_text='Введите текст поста',
        verbose_name='текст поста'
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text='Введите имя',
        verbose_name='автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='группа, к которой будет относиться пост'
    )
    image = models.ImageField(
        'картинка',
        upload_to='posts/',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор'
    )
    text = models.TextField(
        verbose_name='текст комментария',
        help_text='Введите текст комментария'
    )
    created = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created', )
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик',
        help_text='тот кто подписывается'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор',
        help_text='тот на кого подписываются'
    )

    class Meta:
        constraints = (models.UniqueConstraint(
            fields=('author', 'user', ), name='unique pair'), )

    def __str__(self):
        return self.user
