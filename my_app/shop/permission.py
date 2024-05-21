from django.contrib.auth.models import User
from .models import Item  # Thay thế bằng lớp quyền hạn của bạn

admin_user = User.objects.get(username='super')

if not admin_user.has_perm('shop.add_item'):
    # Cấp quyền nếu cần thiết
    permission = Item()
    permission.assign_user(admin_user)