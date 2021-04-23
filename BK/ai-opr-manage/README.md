### 项目说明

#### 1、目录结构

```python
operate_manage_platform/ 
├── README.md （项目说明）
├── app 
│   ├── __init__.py
│   ├── admin.py
│   ├── migrations （数据库迁移文件）
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   ├── utils (工具文件目录：包含 数据 抓取 清洗 入库)
│   ├── models.py （数据库模型）
│   ├── tests.py
│   ├── urls.py（app 内路由）
│   └── views（视图目录）
│       ├── __init__.py
│       └── views.py（视图文件，按模块划分，多个模块多个视图文件）
├── manage.py（项目启动文件）
├── operate_manage_platform
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py（项目配置文件）
│   ├── local_settings.py（无法共享的本地配置，已在gitignore中忽略）
│   ├── urls.py（总路由）
│   └── wsgi.py
├── requirements.txt（项目依赖文件）
└── static（静态文件，前端编译后文件存储位置）
    └── index.html
```

#### 2、开发流程

```python


#local_settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'operate_manage_platform',
        'USER': 'root',
        'PASSWORD': '0404',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


# 如涉及数据库修改，需告知岳彩明统一修改
# 如有自用组件，在app目录下创建目录
# 无法共享的本地配置（包含数据库配置，写入local_settings.py）
```

