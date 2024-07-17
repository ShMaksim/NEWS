from django.contrib.auth.models import User
from news.models import *

# 1
user1 = User.objects.create_user('Tom')
user2 = User.objects.create_user('Jerry')
# 2
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)
# 3
category1 = Category.objects.create(name='Sport')
category2 = Category.objects.create(name='Politics')
category3 = Category.objects.create(name='Education')
category4 = Category.objects.create(name='Technology')
# 4
post1 = Post.objects.create(author=author1, post_type='article', title='article1', text='article1text')
post2 = Post.objects.create(author=author1, post_type='article', title='article2', text='article2text')
post3 = Post.objects.create(author=author2, post_type='news', title='news1', text='news1text')
# 5
post1.categories.add(category1, category2)
post2.categories.add(category3)
post3.categories.add(category4)
# 6
comment1 = Comment.objects.create(post=post1, user=user2, text='Nice')
comment2 = Comment.objects.create(post=post2, user=user1, text='Good')
comment3 = Comment.objects.create(post=post3, user=user1, text='Thanks')
comment4 = Comment.objects.create(post=post2, user=user2, text='Good job')
# 7
post1.like()
post1.like()
post2.like()
post2.like()
post2.dislike()
comment1.like()
comment2.like()
comment3.dislike()
comment4.like()
# 8
author1.update_rating()
author2.update_rating()
print(author1.rating)
print(author2.rating)
# 9
best_author = Author.objects.order_by('-rating').first()
print(f'Best author: {best_author.user.username}, Rating: {best_author.rating}')
# 10
best_post = Post.objects.order_by('-rating').first()
print(f'Date: {best_post.created_at}')
print(f'Author: {best_post.author.user.username}')
print(f'Rating: {best_post.rating}')
print(f'Title: {best_post.title}')
print(f'Preview: {best_post.preview()}')

best_post_comments = Comment.objects.filter(post=best_post)
for comment in best_post_comments:
    print(
        f'Comment Date: {comment.created_at}, User: {comment.user.username}, Rating: {comment.rating}, Text: {comment.text}')
