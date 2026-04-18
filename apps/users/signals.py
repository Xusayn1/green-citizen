from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from apps.users.models.users import User, Role


@receiver(m2m_changed, sender=User.roles.through)
def clear_user_cache_on_role_change(sender, instance, action, **kwargs):
    """Clear user permission cache when roles are added/removed"""
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.clear_permission_cache()


@receiver(m2m_changed, sender=Role.permissions.through)
def clear_role_users_cache(sender, instance, action, **kwargs):
    """Clear cache for all users with this role when role permissions change"""
    if action in ['post_add', 'post_remove', 'post_clear']:
        for user in instance.users.all():
            user.clear_permission_cache()