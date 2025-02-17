from django.shortcuts import render
from .models import Comment
from .serializers import CommentSerializer, CommentUpdateSerializer
from rest_framework import generics, serializers
from Innovation_WebApp.models import Events
from django.contrib.auth.models import User
from uuid import UUID

# Create your views here.
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


    def perform_create(self, serializer):
        post_id = serializer.validated_data.get('post')
        users_id = serializer.validated_data.get('user')

        if post_id is None:
            raise serializers.ValidationError("Post ID is required.")
        if users_id is None:
            raise serializers.ValidationError("User ID is required.")

        print(f"Received post_id: {post_id} of type {type(post_id)}, user_id: {users_id} of type {type(users_id)}")

        try:
            post = Events.objects.get(id=post_id)
        except Events.DoesNotExist:
            raise serializers.ValidationError({"error": f"Invalid post. No event with id {post_id} exists."})

        try:
            print(users_id)
            user = User.objects.get(user_id=users_id)
        except User.DoesNotExist:
            print(users_id)
            user = User.objects.get(user_id=users_id)
            raise serializers.ValidationError({"error": f"Invalid user. No user with id {users_id} exists."})

        serializer.save(post=post, user=user)

# Update a Comment
class CommentUpdateView(generics.UpdateAPIView):
    serializer_class = CommentUpdateSerializer

    def get_object(self):
        comment_id = self.request.data.get('id')
        user_id = self.request.data.get('user')
        
        if not comment_id:
            raise serializers.ValidationError({"id": "This field is required."})
        if not user_id:
            raise serializers.ValidationError({"user": "This field is required."})

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            raise serializers.ValidationError({"error": "Comment not found."})

        try:
            user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
            user = User.objects.get(user_id=user_uuid)
            
            if comment.user.user_id != user.user_id:
                raise serializers.ValidationError({"authorization": "You are not authorized to edit this comment."})
            return comment
        except (User.DoesNotExist, ValueError):
            raise serializers.ValidationError({"user": "User not found."})
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

    def perform_update(self, serializer):
        # The user field will now be a NormalUser instance thanks to validate_user
        serializer.save()
        

# Delete a Comment
class CommentDeleteView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    

    def get_object(self):
        comment_id = self.request.data.get('id')
        if not comment_id:
            raise serializers.ValidationError({"id": "This field is required."})

        try:
            comment = Comment.objects.get(id=comment_id, user=self.request.user)
        except Comment.DoesNotExist:
            raise serializers.ValidationError({"id": "Comment not found or you do not have permission to delete it."})

        return comment
    # Get all Comments
class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for comment in response.data['results']:
            comment_instance = Comment.objects.get(text=comment['text'])
            comment['id'] = comment_instance.id
            comment['user'] = comment_instance.user.user_id
            comment['post'] = comment_instance.post.id
        return response
