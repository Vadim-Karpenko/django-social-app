from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import ImageCreateForm, CommentForm
from .models import Image, Comment
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from actions.utils import create_action, delete_action
from actions.models import Action
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from itertools import chain

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST,
                                files=request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            create_action(request.user, 'Load new image', new_item)
            messages.success(request, 'Photo was added successfuly')
            return redirect(new_item.get_absolute_url())
        else:
            messages.error(request, 'Error adding your image')
    else:
        form = ImageCreateForm(instance=request.user)
    return render(request, 'images/image/create.html', {'form': form})

@login_required
def image_delete(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id, user=request.user)
            if action == 'delete':
                request.user.actions.get(target_id=image.id).delete()
                image.comments.all().delete()
                image.clear_thumbnails()
                image.image.delete()
                image.delete()
                #create_action(request.user, 'likes', image)
            else:
                pass
            return redirect('list')
        except:
            pass
    return redirect('images:list')

def image_detail(request, id):
        image = get_object_or_404(Image, id=id)
        comments = image.comments.filter(active=True)

        # if user not authenticated his name will be set to "Anonymous"
        # and he will not available to leave comment
        if request.user.is_authenticated:
            if request.method == 'POST':
                # A comment was posted
                comment_form = CommentForm(data=request.POST)

                if comment_form.is_valid():
                    # Create Comment object but don't save to database yet
                    new_comment = comment_form.save(commit=False)
                    # Assign the current post to the comment
                    new_comment.image = image
                    new_comment.user = request.user
                    # Save the comment to the database
                    new_comment.save()
            else:
                comment_form = CommentForm()

            #if user not already saw this image
            if request.user not in image.users_view.all():
                #increment total image views by 1
                image.users_view.add(request.user)
            return render(request, 'images/image/detail.html',
                                    {'image': image,
                                     'section': 'images',
                                     'your_name': request.user.profile.get_full_name,
                                     'comments': comments,
                                     'comment_form': comment_form})
        return render(request, 'images/image/detail.html',
                                {'image': image,
                                 'section': 'images',
                                 'your_name': 'Anonymous',
                                 'comments': comments})



@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ko'})

@login_required
def image_list(request):
    following_ids = request.user.following.values_list('id', flat=True)
    page = request.GET.get('page', 1)
    actions = Action.objects.all()

    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
        your_actions = Action.objects.filter(user=request.user)
        actions = list(chain(actions, your_actions))

    paginator = Paginator(actions, 10)

    try:
        actions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer return first page
        actions = paginator.page(1)
    return render(request,
                  'images/image/list.html',
                   {'section': 'images', 'actions': actions, 'following_ids':following_ids})

@login_required
def news_following_error(request):
    return render(request, 'errors/following_error.html', {})
