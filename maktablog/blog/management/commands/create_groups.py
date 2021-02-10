"""
Create permission groups
Create permissions (read only) to models for a set of groups
"""
import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

# group_permission = group_permissions.add(group=group, permission=permission)
#
# group_permission = group.group_permissions_set.add(permission=permission)
#
# group_permission = group.permissions_set.add(permission=permission)
# GROUPS = ['مدیر', 'نویسنده', 'ویراستار', 'ساده']
PERMISSION_GROUPS = {

    'ساده': {'post': ['view'],
             'comment': ['add', 'view'],
             'like': ['add', 'view']},

    'ویراستار': {'post': ['view', 'change'],
                 'comment': ['add', 'view', 'change'],
                 'like': ['add', 'view']},
    'نویسنده': {'post': ['view', 'change', 'add', 'delete'],
                'comment': ['add', 'view', 'change'],
                'like': ['add', 'view']},

}

MODELS = ['post', 'comment', 'like']


class Command(BaseCommand):
    help = 'Creates read only default permission groups for users'

    def handle(self, *args, **options):
        try:
            permissions_list = Permission.objects.all()
            manage_group, created = Group.objects.get_or_create(name='مدیر')
            manage_group.permissions.set(permissions_list)
        except:
            raise Exception("Err")
        for group, val in PERMISSION_GROUPS.items():
            new_group, created = Group.objects.get_or_create(name=group)
            for model, perm in val.items():
                for permission in perm:
                    name = 'Can {} {}'.format(permission, model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue

                    new_group.permissions.add(model_add_perm)

        print("Created default group and permissions.")
