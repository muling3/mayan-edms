��    T      �  q   \            !  !   9  "   [  �   ~  �   -  B  !	  �   d
    1  s  I  d   �    "  �   /  "   �  +  �  �     #  �  :        O     W    _  �   b  2  �  u    Z   �  ^   �  8   K  �   �  �   0  C     �   L  2    �   D!  �  9"  b   �#  �  ($     �%     �&     �&     �&     �&     �&     �&     '  �   '     �'     �'     �'  
   �'  	   �'  	   �'  
   �'  )   �'     (  F   (     Z(  (   _(     �(     �(     �(     �(     �(  d   �(     O)  2   b)  P   �)     �)    �)  O   +  H   V+  @   �+  ^   �+  :   ?,    z,     �-     �-     �-     �-  '   �-     .     .  x  .  �   �/    10  �  N1     �2  ,   �2  ,   &3  �   S3    4  �  -5    �6  n  �7  �  F9  s   ;  �  z;  �   (?  3   �?    @    �B  d  �C  X   �D     JE     SE  #  _E  �   �F  �  +G  �  �H  u   |J  |   �J  [   oK  �   �K    �L  X   �M  �   �M  �  �N    �R  �  �S  |   �U  �  \V  -  <X     jY     qY     xY     �Y     �Y  "   �Y     �Y  �   �Y  
   �Z     �Z     �Z     �Z     �Z     �Z     �Z  5   �Z     [  �   '[     �[  <   �[     \      \     6\     U\     ]\  j   z\  $   �\  K   
]  [   V]     �]  1  �]  h   �^  S   b_  E   �_  k   �_  ?   h`  K  �`  &   �a     b     6b     Sb  8   Yb     �b     �b  �  �b  �   qd  =  e     /   4          #           O   B   F   Q   )      N   M          A           D      0   *                @   ;       .   I              8      %   5   P       7                     '   C             K       6          S       &      
      -           !   <       3   +   1   9   ?      (   2          ,   J            "          :          >      =              L           $              E   	   H   G   T         R    "%s" not a valid entry. %(count)d setting value reverted. %(count)d settings value reverted. A boolean that specifies whether to use the X-Forwarded-Host header in preference to the Host header. This should only be enabled if a proxy which sets this header is in use. A boolean that specifies whether to use the X-Forwarded-Port header in preference to the SERVER_PORT META variable. This should only be enabled if a proxy which sets this header is in use. USE_X_FORWARDED_HOST takes priority over this setting. A dictionary containing the settings for all databases to be used with Django. It is a nested dictionary whose contents map a database alias to a dictionary containing the options for an individual database. The DATABASES setting must configure a default database; any number of additional databases may also be specified. A dictionary containing the settings for all storages to be used with Django. It is a nested dictionary whose contents map a storage alias to a dictionary containing the options for an individual storage. A list of IP addresses, as strings, that: Allow the debug() context processor to add some variables to the template context. Can use the admindocs bookmarklets even if not logged in as a staff user. Are marked as "internal" (as opposed to "EXTERNAL") in AdminEmailHandler emails. A list of all available languages. The list is a list of two-tuples in the format (language code, language name) for example, ('ja', 'Japanese'). This specifies which languages are available for language selection. Generally, the default value should suffice. Only set this setting if you want to restrict language selection to a subset of the Django-provided languages.  A list of authentication backend classes (as strings) to use when attempting to authenticate a user. A list of strings representing the host/domain names that this site can serve. This is a security measure to prevent HTTP Host header attacks, which are possible even under many seemingly-safe web server configurations. Values in this list can be fully qualified names (e.g. 'www.example.com'), in which case they will be matched against the request's Host header exactly (case-insensitive, not including port). A value beginning with a period can be used as a subdomain wildcard: '.example.com' will match example.com, www.example.com, and any other subdomain of example.com. A value of '*' will match anything; in this case you are responsible to provide your own validation of the Host header (perhaps in a middleware; if so this middleware must be listed first in MIDDLEWARE). A list of trusted origins for unsafe requests (e.g. POST). https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-CSRF_TRUSTED_ORIGINS A short text used as the tag name. A string representing the language code for this installation. This should be in standard language ID format. For example, U.S. English is "en-us". It serves two purposes: If the locale middleware isn't in use, it decides which translation is served to all users. If the locale middleware is active, it provides a fallback language in case the user's preferred language can't be determined or is not supported by the website. It also provides the fallback translation when a translation for a given literal doesn't exist for the user's preferred language. A string representing the time zone for this installation. Note that this isn't necessarily the time zone of the server. For example, one server may serve multiple Django-powered sites, each with a separate time zone setting. A tuple representing a HTTP header/value combination that signifies a request is secure. This controls the behavior of the request object’s is_secure() method. Warning: Modifying this setting can compromise your site’s security. Ensure you fully understand your setup before changing it. Cannot revert setting. Setting value has not been updated. Choices Default Default: '' (Empty string). Password to use for the SMTP server defined in EMAIL_HOST. This setting is used in conjunction with EMAIL_HOST_USER when authenticating to the SMTP server. If either of these settings is empty, Django won't attempt authentication. Default: '' (Empty string). Username to use for the SMTP server defined in EMAIL_HOST. If empty, Django won't attempt authentication. Default: '/accounts/login/' The URL where requests are redirected for login, especially when using the login_required() decorator. This setting also accepts named URL patterns which can be used to reduce configuration duplication since you don't have to define the URL in two places (settings and URLconf). Default: '/accounts/profile/' The URL where requests are redirected after login when the contrib.auth.login view gets no next parameter. This is used by the login_required() decorator, for example. This setting also accepts named URL patterns which can be used to reduce configuration duplication since you don't have to define the URL in two places (settings and URLconf). Default: 'django.contrib.sessions.backends.db'. Controls where Django stores session data. Default: 'django.core.mail.backends.smtp.EmailBackend'. The backend to use for sending emails. Default: 'localhost'. The host to use for sending email. Default: 'sessionid'. The name of the cookie to use for sessions.This can be whatever you want (as long as it's different from the other cookie names in your application). Default: 'webmaster@localhost' Default email address to use for various automated correspondence from the site manager(s). This doesn't include error messages sent to ADMINS and MANAGERS; for that, see SERVER_EMAIL. Default: 25. Port to use for the SMTP server defined in EMAIL_HOST. Default: 2621440 (i.e. 2.5 MB). The maximum size (in bytes) that an upload will be before it gets streamed to the file system. See Managing files for details. See also DATA_UPLOAD_MAX_MEMORY_SIZE. Default: 2621440 (i.e. 2.5 MB). The maximum size in bytes that a request body may be before a SuspiciousOperation (RequestDataTooBig) is raised. The check is done when accessing request.body or request.POST and is calculated against the total request size excluding any file upload data. You can set this to None to disable the check. Applications that are expected to receive unusually large form posts should tune this setting. The amount of request data is correlated to the amount of memory needed to process the request and populate the GET and POST dictionaries. Large requests could be used as a denial-of-service attack vector if left unchecked. Since web servers don't typically perform deep request inspection, it's not possible to perform a similar check at that level. See also FILE_UPLOAD_MAX_MEMORY_SIZE. Default: False. Whether to use a TLS (secure) connection when talking to the SMTP server. This is used for explicit TLS connections, generally on port 587. If you are experiencing hanging connections, see the implicit TLS setting EMAIL_USE_SSL. Default: False. Whether to use an implicit TLS (secure) connection when talking to the SMTP server. In most email documentation this type of TLS connection is referred to as SSL. It is generally used on port 465. If you are experiencing problems, see the explicit TLS setting EMAIL_USE_TLS. Note that EMAIL_USE_TLS/EMAIL_USE_SSL are mutually exclusive, so only set one of those settings to True. Default: None. Specifies a timeout in seconds for blocking operations like the connection attempt. Default: None. The URL where requests are redirected after a user logs out using LogoutView (if the view doesn't get a next_page argument). If None, no redirect will be performed and the logout view will be rendered. This setting also accepts named URL patterns which can be used to reduce configuration duplication since you don't have to define the URL in two places (settings and URLconf). Default: [] (Empty list). List of compiled regular expression objects representing User-Agent strings that are not allowed to visit any page, systemwide. Use this for bad robots/crawlers. This is only used if CommonMiddleware is installed (see Middleware). Django Edit Edit setting: %s Edit settings English Enter the new setting value. Global name Local storage is currently disabled, changes to settings will not be saved. Instead, use environment variables to modify settings. Modified Name Namespace: %s, not found Namespaces New value Old value Overridden Possible values allowed for this setting. Revert Revert the selected setting value? Revert the selected settings value? Save Save settings to the configuration file? Setting count Setting namespaces Setting updated successfully. Settings Settings in namespace: %s Settings inherited from an environment variable take precedence and cannot be changed in this view.  Settings namespace Settings saved to configuration file successfully. Settings updated. Save and restart your installation for changes to take effect. Smart settings The full Python path of the WSGI application object that Django's built-in servers (e.g. runserver) will use. The django-admin startproject management command will create a simple wsgi.py file with an application callable in it, and point this setting to that application. The list of validators that are used to check the strength of user's passwords. The value of the setting is being overridden by an environment variable. The value of this setting being modified since the last restart. This setting is overridden by an environment variable, changing its value will have no effect. This will overwrite the content of the configuration file. URL to use when referring to static files located in STATIC_ROOT. Example: "/static/" or "http://static.example.com/" If not None, this will be used as the base path for asset definitions (the Media class) and the staticfiles app. It must end in a slash if set to a non-empty value. Unsaved changes will be lost. Updated setting Updated settings Value Value of setting "%(object)s" reverted. View settings Warning When set to True, if the request URL does not match any of the patterns in the URLconf and it doesn't end in a slash, an HTTP redirect is issued to the same URL with a slash appended. Note that the redirect may cause any data submitted in a POST request to be lost. The APPEND_SLASH setting is only used if CommonMiddleware is installed (see Middleware). See also PREPEND_WWW. Whether to store the CSRF token in the user's session instead of in a cookie. https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-CSRF_USE_SESSIONS Whether to use a secure cookie for the CSRF cookie. If this is set to True, the cookie will be marked as "secure", which means browsers may ensure that the cookie is only sent with an HTTPS connection. https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-CSRF_COOKIE_SECURE Project-Id-Version: Mayan EDMS
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2024-05-07 07:30+0000
Last-Translator: Roberto Rosario, 2024
Language-Team: Spanish (https://app.transifex.com/rosarior/teams/13584/es/)
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Language: es
Plural-Forms: nplurals=3; plural=n == 1 ? 0 : n != 0 && n % 1000000 == 0 ? 1 : 2;
 "%s" no es una entrada válida. %(count)d valor de configuración revertido. %(count)d valor de configuración revertido. Un booleano que especifica si se debe usar el encabezado X-Fordered-Host con preferencia al encabezado Host. Esto solo debe habilitarse si se está utilizando un proxy que establece este encabezado. Un booleano que especifica si se debe usar el encabezado X-Fordered-Port con preferencia a la variable SERVER_PORT META. Esto solo debe habilitarse si se está utilizando un proxy que establece este encabezado. USE_X_FORWARDED_HOST tiene prioridad sobre esta configuración. Un diccionario que contiene la configuración de todas las bases de datos que se utilizarán con Django. Es un diccionario anidado cuyos contenidos asignan un alias de base de datos a un diccionario que contiene las opciones para una base de datos individual. La configuración DATABASES debe configurar una base de datos predeterminada; también se puede especificar cualquier cantidad de bases de datos adicionales. Un diccionario que contiene la configuración de todos los almacenamientos que se utilizarán con Django. Es un diccionario multiniveles cuyo contenido asigna un alias de almacenamiento a un diccionario que contiene las opciones para un almacenamiento individual. Una lista de direcciones IP, en forma de texto, que: Permiten que el procesador de contexto debug() agregue algunas variables al contexto de la plantilla. Puede usar los marcadores de Admindocs incluso si no ha iniciado sesión como usuario del personal. Están marcados como 'internos' (a diferencia de 'EXTERNOS') en los correos electrónicos de AdminEmailHandler. Una lista de todos los idiomas disponibles. La lista es una lista de dos tuplas en el formato (código de idioma, nombre del idioma), por ejemplo, ('ja', 'Japonés'). Esto especifica qué idiomas están disponibles para la selección de idiomas. Generalmente, el valor predeterminado debería ser suficiente. Solo establezca esta configuración si desea restringir la selección de idioma a un subconjunto de los idiomas proporcionados por Django. Una lista de clases de backend de autenticación (en forma de texto) para usar al intentar autenticar a un usuario. Una lista de textos que representan los nombres de host / dominio que este sitio puede servir. Esta es una medida de seguridad para evitar los ataques de encabezado HTTP Host, que son posibles incluso bajo muchas configuraciones de servidor web aparentemente seguras. Los valores en esta lista pueden ser nombres totalmente calificados (por ejemplo, 'www.ejemplo.com'), en cuyo caso se compararán exactamente con el encabezado Host de la solicitud (no distingue entre mayúsculas y minúsculas, sin incluir el puerto). Un valor que comienza con un punto se puede usar como un comodín de subdominio: '.example.com' coincidirá con example.com, www.example.com y cualquier otro subdominio de example.com. Un valor de '*' coincidirá con cualquier cosa; en este caso, usted es responsable de proporcionar su propia validación del encabezado de host (quizás en un middleware, si es así, este middleware debe aparecer primero en MIDDLEWARE). Una lista de orígenes confiables para solicitudes inseguras (por ejemplo, POST). https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-CSRF_TRUSTED_ORIGINS Un texto corto usado como el nombre de la etiqueta. Un texto que representa el código de idioma para esta instalación. Esto debe estar en formato de ID de idioma estándar. Por ejemplo, el inglés de EE. UU. Es 'en-us'. Tiene dos propósitos: si el middleware de configuración regional no está en uso, decide qué traducción se sirve a todos los usuarios. Si el middleware de configuración regional está activo, proporciona un idioma alternativo en caso de que el idioma preferido del usuario no se pueda determinar o el sitio web no lo admita. También proporciona la traducción alternativa cuando no existe una traducción para un literal dado para el idioma preferido del usuario. Un text que representa la zona horaria para esta instalación. Tenga en cuenta que esto no es necesariamente la zona horaria del servidor. Por ejemplo, un servidor puede servir múltiples sitios con Django, cada uno con una configuración de zona horaria separada. Una tupla que representa una combinación de encabezado / valor HTTP que significa que una solicitud es segura. Esto controla el comportamiento del método is_secure() del objeto de solicitud. Advertencia: modificar esta configuración puede comprometer la seguridad de su sitio. Asegúrese de comprender completamente su configuración antes de cambiarla. No se puede revertir la configuración. El valor de configuración no se ha actualizado. Opciones Por defecto Valor predeterminado: '' (texto vacío). Contraseña para usar para el servidor SMTP definido en EMAIL_HOST. Esta configuración se usa junto con EMAIL_HOST_USER al autenticarse en el servidor SMTP. Si cualquiera de estas configuraciones está vacía, Django no intentará la autenticación. Valor predeterminado: '' (text vacío). Nombre de usuario a usar para el servidor SMTP definido en EMAIL_HOST. Si está vacío, Django no intentará la autenticación. Valor predeterminado: '/ accounts / login /' La URL donde las solicitudes se redireccionan para iniciar sesión, especialmente cuando se utiliza el decodificador login_required (). Esta configuración también acepta patrones de URL nombrados que se pueden usar para reducir la duplicación de configuración, ya que no tiene que definir la URL en dos lugares (configuración y URLconf). Valor predeterminado: '/ accounts / profile /' La URL donde las solicitudes se redirigen después del inicio de sesión cuando la vista contrib.auth.login no obtiene el siguiente parámetro. Esto es usado por el decorador login_required (), por ejemplo. Esta configuración también acepta patrones de URL nombrados que se pueden usar para reducir la duplicación de configuración, ya que no tiene que definir la URL en dos lugares (configuración y URLconf). Valor predeterminado: "django.contrib.sessions.backends.db". Controla dónde Django almacena los datos de la sesión. Valor predeterminado: 'django.core.mail.backends.smtp.EmailBackend'. El backend para usar para enviar correos electrónicos. Valor predeterminado: 'localhost'. El host que se usará para enviar correos electrónicos. Valor predeterminado: "sessionid". El nombre de la cookie que se utilizará para las sesiones. Puede ser lo que desee (siempre y cuando sea diferente de los otros nombres de cookies en su aplicación). Predeterminado:'webmaster@localhost' Dirección de correo electrónico predeterminada que se usa para la correspondencia automatizada del administrador(es) del sitio. Esto no incluye los mensajes de error enviados a ADMINS y MANAGERS; para eso, vea SERVER_EMAIL. Valor predeterminado: 25. Puerto para usar para el servidor SMTP definido en EMAIL_HOST. Valor predeterminado: 2621440 (es decir, 2,5 MB). El tamaño máximo (en bytes) que una carga será antes de que se transmita al sistema de archivos. Consulte Administración de archivos para más detalles. Ver también DATA_UPLOAD_MAX_MEMORY_SIZE. Valor predeterminado: 2621440 (es decir, 2,5 MB). El tamaño máximo en bytes que puede ser un cuerpo de solicitud antes de que se genere una Operación Sospechosa (RequestDataTooBig). La comprobación se realiza al acceder a request.body o request.POST y se calcula con respecto al tamaño total de la solicitud, excluyendo cualquier archivo de carga de datos. Puede configurar esto en Ninguno para desactivar la verificación. Las aplicaciones que se espera que reciban publicaciones de forma inusualmente grande deben ajustar esta configuración. La cantidad de datos de solicitud se correlaciona con la cantidad de memoria necesaria para procesar la solicitud y llenar los diccionarios GET y POST. Las solicitudes grandes podrían usarse como un vector de ataque de denegación de servicio si no se seleccionan. Dado que los servidores web normalmente no realizan una inspección profunda de solicitudes, no es posible realizar una comprobación similar en ese nivel. Ver también FILE_UPLOAD_MAX_MEMORY_SIZE. Predeterminado: Falso. Si se debe usar una conexión TLS (segura) cuando se habla con el servidor SMTP. Esto se usa para conexiones explícitas de TLS, generalmente en el puerto 587. Si experimenta conexiones suspendidas, consulte la configuración de TLS implícita EMAIL_USE_SSL. Predeterminado: Falso. Si se debe usar una conexión TLS (segura) implícita al hablar con el servidor SMTP. En la mayoría de la documentación de correo electrónico, este tipo de conexión TLS se conoce como SSL. Generalmente se usa en el puerto 465. Si tiene problemas, consulte la configuración de TLS explícita EMAIL_USE_TLS. Tenga en cuenta que EMAIL_USE_TLS / EMAIL_USE_SSL son mutuamente excluyentes, por lo que solo debe establecer una de esas configuraciones en True. Predeterminado: ninguno Especifica un tiempo de espera en segundos para operaciones de bloqueo como el intento de conexión. Predeterminado: Ninguno. La URL donde se redirigen las solicitudes después de que un usuario cierre sesión usando LogoutView (si la vista no obtiene un argumento next_page). Si Ninguno, no se realizará una redirección y se procesará la vista de cierre de sesión. Esta configuración también acepta patrones de URL con nombre que se pueden usar para reducir la duplicación de la configuración, ya que no tiene que definir la URL en dos lugares (configuración y URLconf). Valor predeterminado: [] (lista vacía). Lista de objetos de expresiones regulares compilados que representan textos de User-Agent que no pueden visitar ninguna página, en todo el sistema. Úselo para robots / rastreadores malos. Esto solo se usa si CommonMiddleware está instalado (ver Middleware). Django Editar Editar ajuste: %s Editar ajustes Inglés Ingrese el nuevo valor del ajuste. Nombre global El almacenamiento local está actualmente deshabilitado, los cambios en la configuración no se guardarán. En su lugar, utilice variables de entorno para modificar la configuración. Modificado Nombre Categoría: %s, no encontrada Categorías Nuevo valor Valor antiguo Anulado Posibles valores permitidos para esta configuración. Revertir ¿Revertir el valor de configuración seleccionado? ¿Revertir el valor de las configuraciones seleccionadas? ¿Revertir el valor de configuración seleccionada? Guardar ¿Guardar la configuración en el archivo de configuración? Conteo de ajustes Categoría de ajustes Ajuste actualizado con éxito. Ajustes Ajustes en la categoría: %s La configuración heredada de una variable de entorno tiene prioridad y no se puede cambiar en esta vista. Espacio de nombres de configuración La configuración se guardó correctamente en el archivo de configuración. Ajustes actualizados. Guarde y reinicie su instalación para que los cambios surtan efecto. Ajustes inteligentes La ruta completa de Python del objeto de aplicación WSGI que usarán los servidores incorporados de Django (por ejemplo, runserver). El comando django-admin startproject management creará un archivo wsgi.py simple con una aplicación invocable en él, y señalará esta configuración a esa aplicación. La lista de validadores que se utilizan para verificar la seguridad de las contraseñas de los usuarios. El valor de la configuración está siendo reemplazado por una variable de entorno. El valor de esta configuración modificado desde el último reinicio. Esta configuración es reemplazada por una variable de entorno; cambiar su valor no tendrá ningún efecto. Esto sobrescribirá el contenido del archivo de configuración. URL a usar cuando se hace referencia a archivos estáticos ubicados en STATIC_ROOT. Ejemplo: "/static/" o "http://static.example.com/". Si no es None, se usará como ruta base para las definiciones de activos (la clase Media) y la aplicación staticfiles. Debe terminar en una barra inclinada si se establece en un valor no vacío. Los cambios no guardados se perderán. Configuración actualizada Configuraciones actualizadas Valor Se revirtió el valor de la configuración "%(object)s". Ver configuraciones Advertencia Cuando se establece en True, si la URL de solicitud no coincide con ninguno de los patrones en el URLconf y no termina en una barra inclinada, se emite un redireccionamiento HTTP a la misma URL con una barra inclinada. Tenga en cuenta que la redirección puede hacer que se pierdan los datos enviados en una solicitud POST. La configuración APPEND_SLASH solo se usa si está instalado CommonMiddleware (ver Middleware). Ver también PREPEND_WWW. Si se debe almacenar el token CSRF en la sesión del usuario en lugar de en una cookie. https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-CSRF_USE_SESSIONS Si se debe utilizar una cookie segura para la cookie CSRF. Si se establece en Verdadero, la cookie se marcará como "segura", lo que significa que los navegadores pueden garantizar que la cookie solo se envíe con una conexión HTTPS. https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-CSRF_COOKIE_SECURE 