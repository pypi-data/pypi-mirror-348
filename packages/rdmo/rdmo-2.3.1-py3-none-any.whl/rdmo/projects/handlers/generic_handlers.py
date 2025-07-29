from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site

from rdmo.projects.models import Membership, Project
from rdmo.questions.models import Catalog


def m2m_catalogs_changed_projects_sync_signal_handler(instance, action, pk_set, project_field):

    if action == 'post_remove' and pk_set:
        projects_to_change = (
            Project.objects
                .filter_catalogs(catalogs=Catalog.objects.filter(pk__in=pk_set))
                .filter(**{project_field: instance})
        )
        for project in projects_to_change:  # remove instance from project
            getattr(project, project_field).remove(instance)

    elif action == 'post_clear':
        projects_to_change = Project.objects.filter(**{project_field: instance})
        for project in projects_to_change:  # remove instance from project
            getattr(project, project_field).remove(instance)

    elif action == 'post_add' and pk_set:
        projects_to_change = (
            Project.objects
                .filter_catalogs(catalogs=Catalog.objects.filter(pk__in=pk_set))
                .exclude(**{project_field: instance})
        )
        for project in projects_to_change:  # add instance to project
            getattr(project, project_field).add(instance)


def m2m_sites_changed_projects_sync_signal_handler(instance, action, pk_set, project_field):

    if action == 'post_remove' and pk_set:
        projects_to_change = (
            Project.objects
                .filter_catalogs(catalogs=instance.catalogs.all())
                .filter(site__in=Site.objects.filter(pk__in=pk_set))
                .filter(**{project_field: instance})
        )
        for project in projects_to_change:  # remove instance from project
            getattr(project, project_field).remove(instance)

    elif action == 'post_clear':
        projects_to_change = (
            Project.objects
                .filter_catalogs()
                .filter(**{project_field: instance})
        )
        for project in projects_to_change:  # remove instance from project
            getattr(project, project_field).remove(instance)

    elif action == 'post_add' and pk_set:
        projects_to_change = (
            Project.objects
                .filter_catalogs(catalogs=instance.catalogs.all())
                .filter(site__in=Site.objects.filter(pk__in=pk_set))
                .exclude(**{project_field: instance})
        )
        for project in projects_to_change:  # add instance to project
            getattr(project, project_field).add(instance)


def m2m_groups_changed_projects_sync_signal_handler(instance, action, pk_set, project_field):

    if action == 'post_remove' and pk_set:
        related_groups = Group.objects.filter(pk__in=pk_set)
        users = User.objects.filter(groups__in=related_groups)
        memberships = (
            Membership.objects
                .filter(role='owner', user__in=users)
                .values_list('id', flat=True)
        )
        projects_to_change = (
            Project.objects
                .filter_catalogs(catalogs=instance.catalogs.all())
                .filter(memberships__in=memberships)
                .filter(**{project_field: instance})
        )
        for project in projects_to_change:  # remove instance from project
            getattr(project, project_field).remove(instance)

    elif action == 'post_clear':
        # Remove all linked projects regardless of catalogs
        projects_to_change = (
            Project.objects
                .filter_catalogs()
                .filter(**{project_field: instance})
        )
        for project in projects_to_change:  # remove instance from project
            getattr(project, project_field).remove(instance)

    elif action == 'post_add' and pk_set:
        related_groups = Group.objects.filter(pk__in=pk_set)
        users = User.objects.filter(groups__in=related_groups)
        memberships = (
            Membership.objects
                .filter(role='owner', user__in=users)
                .values_list('id', flat=True)
        )
        projects_to_change = (
            Project.objects
                .filter_catalogs(catalogs=instance.catalogs.all())
                .filter(memberships__in=memberships)
                .exclude(**{project_field: instance})
        )
        for project in projects_to_change:  # add instance to project
            getattr(project, project_field).add(instance)
