# Dseagull

可快速构建 RESTful API, 简化配置, 减少代码:

✅ 通过一行命令创建数据模型, 及对应的 serializer, viewset, routers 和 testcase

✅ 省去配置 REST_FRAMEWORK, 默认配置分页类, 文档类等

✅ 简化 JWT

✅ 接口数据校验器支持中文提示

✅ 接口过滤支持时间范围查询

✅ 接口全局 request_id 的自动生成

✅ 接口 500 异常时, 报警通知到钉钉

✅ 中间件请求日志默认输出

✅ 提供基础的数据模型

✅ 支持 SAE 健康检测

❌ 接口默认用户身份认证

❌ 接口默认进行权限判断

❌ 统一的日志格式输出

❌ 支持 SAE 的发布命令

---

# INSTALLED_APPS

添加 dseagull 到 INSTALLED_APPS 中, 注意必须要放在 rest_framework 前面

```
INSTALLED_APPS = [
    ...
    'dseagull',
    'rest_framework',
]
```

---

# MIDDLEWARE

添加 dseagull.logger.LoggerMiddleware 到 MIDDLEWARE 中, 用于收集日志的字段

```
MIDDLEWARE = [
    'dseagull.logger.LoggerMiddleware',
    ...
]
```

---

添加 dseagull.middleware.BaseMiddleware 到 MIDDLEWARE 中, 用于请求的基本输出

```
MIDDLEWARE = [
    'dseagull.middleware.BaseMiddleware',
    ...
]
```

---

# REST_FRAMEWORK

不需要配置 REST_FRAMEWORK, 默认配置如下:

```
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'dseagull.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    
}
```

---

# models.BaseModel

提供基础模型, 添加了 created, updated

    from django.db import models
    
    
    class BaseModel(models.Model):
        class Meta:
            abstract = True
    
        created = models.DateTimeField(
            auto_now_add=True, verbose_name='创建时间', db_index=True,
        )
        updated = models.DateTimeField(
            auto_now=True, verbose_name='更新时间', db_index=True,
        )

---

# serializers.Field

支持 required=True 时提示带上字段的 help_text 信息

    from rest_framework.serializers import Serializer
    class ExampleSerializer(Serializer):
        name = field(help_text='姓名')
    ExampleSerializer(data={}).is_valid()

原本提示:这个字段是必填项。

现提示:姓名:这个字段是必填项。

---

支持 required=True, null=False 时提示带上字段的 help_text 信息

    from rest_framework.serializers import Serializer
    class ExampleSerializer(Serializer):
        name = field(help_text='姓名')
    ExampleSerializer(data={'name': None}).is_valid()

原本提示:This field may not be null.
现提示:姓名:不能为空。

---

支持 required=True, null=False 时提示带上字段的 help_text 信息

    from rest_framework.serializers import Serializer
    class ExampleSerializer(Serializer):
        name = field(help_text='姓名')
    ExampleSerializer(data={'name': ''}).is_valid()

原本提示:This field may not be blank.
现提示:姓名:不能为空白。

---

为了避免和 /docs 展示区分, 也可以使用 error_help_text 和 help_text 区分

    from rest_framework.serializers import Serializer
    class ExampleSerializer(Serializer):
        name = field(help_text='姓名(string)', error_help_text="姓名")
    ExampleSerializer(data={'name': ''}).is_valid()

原本提示:This field may not be blank.
现提示:姓名:不能为空白。

/docs 中则展示 姓名(string)

---

# Filters

支持时间区间的查询

    from dseagull.filters import BaseFilterSet
    class PersonFilter(BaseFilterSet):
        last_name = filters.CharFilter()
        created = filters.CharFilter(method='filter_datetime', )
    
        class Meta:
            model = Person
            fields = ('id',)

在查询时, 参数输入 /?created=1738771200,1738771201 即可过滤出对应的数据

---

# Commands

## startmodel

    python manage.py startmodel -n Apple

执行上面的命令, 可以自动创建和修改标准化的 model, serializer, viewset, routers

---

# JWT

简化对称加密型的 JWT 编码和解码的过程, 需要配置 JWT_KEY 和 JWT_EXP

    from dseagull.djwt import JWTHS256
    token = JWTHS256().encode({'username': 'admin'})
    payload = JWTHS256().decode(token)

---

# Settings

---

## 报警

---
支持接口 500 异常的钉钉报警: DJANGO_REQUEST_ERROR_WEBHOOK 可配置钉钉报警的 webhook
同样支持手动触发报警:

    from dseagull.dlogging import LOGGER
    LOGGER.error("异常提示")

---

# SAE

配置健康检测接口, 配置如下, 即可访问 /sae/checkpreload , 响应内容为 successful

    from dseagull.sae import include_sae_urls
    urlpatterns = [
        url(r'^sae/', include_sae_urls()),
    ]

---
