from django.urls import reverse
from django.shortcuts import redirect

import re

def up_vote_down_vote_helper(request, post):
    """
    Redirects user back to either a user profile or comments page
    When the user up_vote or down_voted a foodie on either pages
    """

    referer = request.META['HTTP_REFERER']
    
    comment_search = re.search(r'/comments/post/', referer)
    
    if comment_search:
        print(f"reeust, {referer}")
        print("END")
        return redirect(reverse('fapp:comments', kwargs={'pk': post.id }))
    
    profile_search = re.search(r'/profile/', referer)

    if profile_search:
        user_id = referer[-1:]
        return redirect(reverse('fapp:profile', kwargs={'pk':user_id}))
    
    return redirect(reverse("fapp:home") + f"#{post.id}")
    
