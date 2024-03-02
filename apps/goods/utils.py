from apps.goods.get import get_categories
from django.conf import settings
from django.template import loader
import os
import time

def generate_static_list_search_html():
    """
    生成静态的商品列表页和搜索结果页html文件
    """
    # 商品分类菜单
    categories = get_categories()

    # 渲染模板，生成静态html文件
    print('%s: generate_static_index_html' % time.ctime())
    context = {
        'categories': categories,
    }

    template = loader.get_template('list.html')
    html_text = template.render(context)
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'list.html')
    with open(file_path,'w', encoding='utf-8') as f:
        f.write(html_text)