import os
import sys
import subprocess

# no tocar 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#   ---------------------------------------------------------------------------

import utils.variable_globals as va
import utils.helpers_command_global as helper

class DjangoFuncionApp:
    def __init__(self, project_root, project_name):
        self.project_root = project_root
        self.project_name = project_name
        self.home = "home"

    async def create_apps(self):
        app_path = os.path.join(self.project_root, self.home)
        print(f"🚀 Creando app '{self.home}' en {app_path}")

        try:
            subprocess.run(
                ["python", "manage.py", "startapp", self.home],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al crear la app con manage.py: {e}")
            return
        
        steps = [
            ("Instalando URLs y vistas de perfil", self.install_url_and_views_perfil),
            ("Instalando templates y archivos estáticos", self.install_templates_and_static_files),
            ("Creando carpeta services y archivos", self.create_carpet_services_and_files),
            ("Creando carpeta utils y archivos", self.carpet_utils_and_files),
            ("Creando carpeta test y archivos", self.create_carpet_test_and_files),
            ("Creando carpeta templatetags y archivos", self.create_templatetags),
            ("Configurando installed_apps", self.installed_apps),
            ("Configurando urls del proyecto", self.installed_url_in_project),
        ]

        for description, coroutine in steps:
            try:
                print(f"🔧 {description}...")
                await coroutine()
                print(f"✅ {description} completado")
            except Exception as e:
                print(f"⚠️ Error durante '{description}': {e}")
        print(f"✅ App '{self.home}' creada exitosamente en {app_path}")

    async def installed_apps(self):
        settings_path = os.path.join(self.project_name, "settings.py")
        if not os.path.exists(settings_path):
            print(f"No se encontró el archivo settings.py en {settings_path}")
            return
        
        with open(settings_path, 'r') as f:
            lines = f.readlines()

        app_already_installed = any(f"'{self.home}'" in line for line in lines)
        if app_already_installed:
            print(f"La app '{self.home}' ya está instalada en INSTALLED_APPS.")
            return

        new_lines = []
        inside_installed_apps = False
        for line in lines:
            new_lines.append(line)
            if "INSTALLED_APPS" in line and '=' in line:
                inside_installed_apps = True
            elif inside_installed_apps and line.strip().startswith(']'):
                new_lines.insert(-1, f"    '{self.home}',\n")
                inside_installed_apps = False

        with open(settings_path, 'w') as f:
            f.writelines(new_lines)

        print(f"✅ App '{self.home}' agregada a INSTALLED_APPS en settings.py.")
        await self.write_variables()

    async def write_variables(self):
        settings_path = os.path.join(self.project_name, "settings.py")
        if not os.path.exists(settings_path):     
            print(f"No se encontró el archivo settings.py en {settings_path}")
            return

        with open(settings_path, 'a') as f:
            f.write(va.config_variables.strip())
        print("✅ Variables globales y de configuración de email agregadas a settings.py.")

    async def installed_url_in_project(self):
        urls_path = os.path.join(self.project_name, "urls.py")

        if not os.path.exists(urls_path):
            print(f"No se encontró el archivo urls.py en {urls_path}")
            return

        with open(urls_path, 'r') as f:
            lines = f.readlines()

        # Verificar si ya existen
        has_include_import = any("include" in line and "django.urls" in line for line in lines)
        has_home_url = any("include('perfil.urls')" in line for line in lines)
        has_accounts_url = any("include('django.contrib.auth.urls')" in line for line in lines)

        new_lines = []
        for line in lines:
            # Si encontramos el import sin include, lo corregimos
            if "from django.urls import path" in line and "include" not in line:
                line = line.strip().replace("path", "path, include") + "\n"
            new_lines.append(line)

        # Si falta el import, lo agregamos
        if not has_include_import:
            for i, line in enumerate(new_lines):
                if "from django.urls" in line:
                    new_lines.insert(i + 1, "from django.urls import include\n")
                    break
            else:
                new_lines.insert(0, "from django.urls import path, include\n")

        # Agregar las rutas dentro de urlpatterns
        for i, line in enumerate(new_lines):
            if "urlpatterns" in line and "=" in line:
                # Buscamos donde empieza la lista [
                for j in range(i, len(new_lines)):
                    if "[" in new_lines[j]:
                        insert_index = j + 1
                        break
                else:
                    insert_index = i + 1  # Por si no encuentra
                if not has_home_url:
                    new_lines.insert(insert_index, f"    path('', include('{self.home}.urls')),\n")
                    insert_index += 1
                if not has_accounts_url:
                    new_lines.insert(insert_index, "    path('accounts/', include('django.contrib.auth.urls')),\n")
                break

        with open(urls_path, 'w') as f:
            f.writelines(new_lines)

        print("✅ URLs de 'perfil' y 'accounts' agregadas exitosamente a urls.py.")

    async def install_url_and_views_perfil(self):
        file_archive_urls =  os.path.join(self.home, 'urls.py')
        file_archive_views = os.path.join(self.home, 'views.py')
        file_archive_forms = os.path.join(self.home, 'forms.py')

        with open(file_archive_urls, 'w') as f:
            f.write(va.urls_home.strip())

        with open(file_archive_views, 'w') as f:
            f.write(va.views.strip())

        with open(file_archive_forms, 'w') as f:
            f.write(va.forms_home.strip())
        
        print(f"✅  configuracion de views y urls de {self.home}, terminada")

    async def install_templates_and_static_files(self):
        # base_path = carpeta donde está este archivo (dentro de services)
        base_path = os.path.abspath(os.path.dirname(__file__))

        # Subir un nivel para salir de 'services'
        project_root = os.path.dirname(base_path)

        # Ahora apuntamos fuera de 'services'
        views_path = os.path.join(project_root, 'views')
        print(f"📁 Buscando en: {views_path}")

        """if not os.path.exists(views_path):
            os.makedirs(views_path, exist_ok=True)
            print("Carpeta 'views' creada fue crada.'")

            file_init_ = os.path.join(views_path, '__init__.py')
            with open(file_init_, 'w') as f:
                f.write('')
            print("Archivo '__init__.py' creado dentro de 'views'.")
        else:
            print("La carpeta 'views' ya existe fuera de 'services'.") """
        
        #rutas de origen
        templates_path = os.path.join(views_path, 'templates')
        static_path = os.path.join(views_path, 'static')

        #rutas de destino
        dest_templates = os.path.join(self.home, 'templates')
        dest_static = os.path.join(self.home, 'static')


        #creacion de las carpetas
        os.makedirs(dest_templates, exist_ok=True)
        os.makedirs(dest_static, exist_ok=True)

        # Copiar templates (.html)
        helper.copy_recursive(templates_path, dest_templates, extension=['.html'])

        # Copiar archivos estáticos (.css, .js, imágenes si quieres)
        helper.copy_recursive(os.path.join(static_path, 'css'), os.path.join(dest_static, 'css'), extension=['.css'])
        helper.copy_recursive(os.path.join(static_path, 'js'), os.path.join(dest_static, 'js'), extension=['.js'])
        # Puedes agregar más extensiones si quieres: ['.css', '.js', '.png', '.jpg']
        print("✅ archivos de las carpetas static y templates hechos corectamente ")

    async def create_carpet_services_and_files(self):
        carpet_services = os.path.join(self.home, 'services')
        if not os.path.exists(carpet_services):
            print("📁 creando la carpeta services")
            os.makedirs(carpet_services, exist_ok=True)
        else:
            print("⚠️ la carpeta ya existe")

        file_user_password = os.path.join(carpet_services, 'user_password.py')
        file_user_profile = os.path.join(carpet_services, 'user_profile.py')

        helper.copy_content(file_user_profile, va.user_profile, 'user_profile.py')
        helper.copy_content(file_user_password, va.user_password, 'user_password.py')

        print("✅ terminado los archivos de la carpeta services")

    async def carpet_utils_and_files(self):
        carpet_utils = os.path.join(self.home, 'utils')
        if not os.path.exists(carpet_utils):
            print("📁 creando la carpeta utils")
            os.makedirs(carpet_utils, exist_ok=True)
            file_init_ = os.path.join(carpet_utils, '__init__.py')
            with open(file_init_, 'w') as f:
                f.write('')
            print("✅ Archivo '__init__.py' creado dentro de 'utils'.")
        else:
            print("⚠️ la carpeta ya existe")

        file_test_helpers = os.path.join(carpet_utils, 'test_helpers.py')
        
        helper.copy_content(file_test_helpers, va.test_helpers, 'test_helpers.py')

        print(f"✅ creada la carpeta {carpet_utils}, y sus archivos")

    async def create_carpet_test_and_files(self):
        carpet_test = os.path.join(self.home, 'test')

        if not os.path.exists(carpet_test):
            print("📁 creando la carpeta test")
            os.makedirs(carpet_test, exist_ok=True)
            file_init_ = os.path.join(carpet_test, '__init__.py')
            with open(file_init_, 'w') as f:
                f.write('')
            print("✅ Archivo '__init__.py' creado dentro de 'test'.")
        else:
            print("⚠️ la carpeta ya existe")
        
        file_test_profile = os.path.join(carpet_test, 'test_profile.py')
        file_test_password = os.path.join(carpet_test, 'test_password.py')

        helper.copy_content(file_test_profile, va.test_profile, 'test_profile.py')
        helper.copy_content(file_test_password, va.test_password, 'test_password.py')

        print("✅ creada la carpeta de test y sus archivos")

    async def create_templatetags(self):
        carpet_templatetags = os.path.join(self.home, 'templatetags')
        if not os.path.exists(carpet_templatetags):
            print("📁 creando la carpeta templatetags")
            os.makedirs(carpet_templatetags, exist_ok=True)
            file_init_ = os.path.join(carpet_templatetags, '__init__.py')
            with open(file_init_, 'w') as f:
                f.write('')
            print("✅ Archivo '__init__.py' creado dentro de 'templatetags'.")
        else:
            print("⚠️ la carpeta ya existe")

        file_templatetags = os.path.join(carpet_templatetags, 'components.py')

        helper.copy_content(file_templatetags, va.components, 'components.py')

        print("✅ creada la carpeta de los templatetags y sus archivos")
