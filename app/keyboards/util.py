from database.methods import Methods


def get_user_groups_dict(user_id: int) -> dict:
    user = Methods(user_id)
    active_group_id = user.active_group_id

    groups: dict = {
        group.id:
            f"{group.name} "
            f"{'(🔒) ' if group.private else ''} "
            f"{'✅' if group.id == active_group_id else ''}"
        for group in user.user_groups
    }
    return groups