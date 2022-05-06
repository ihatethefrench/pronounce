from flask import Flask, render_template, request
from urllib.request import urlopen
import yaml

app = Flask(
        __name__,
        template_folder='static')

with open("conf.yml", "r") as global_conf_file:
    global_conf = yaml.load(global_conf_file, Loader=yaml.FullLoader)

@app.errorhandler(Exception)
def basic_error(e):
    return render_template(
             'error.html',
             error=e,
             url=request.url,
             conf=global_conf,
             color_bg=
               global_conf['colors']['background'],
             color_fg=
               global_conf['colors']['foreground'],
             color_h=
               global_conf['colors']['heading'],
             color_err=
               global_conf['colors']['text'])

@app.route("/<username>")
def root(username):
    with urlopen(f"{global_conf['user-url']}".replace("{username}", f"{username}")) as data:
        yml = data.read().decode('utf-8')
        conf = yaml.load(yml, Loader=yaml.FullLoader)
    x = conf['colors']['background'] or global_conf['colors']['background']
    print(f"x is {x}")
    return render_template(
             'index.html',
             color_bg=
               conf['colors']['background'] or global_conf['colors']['background'],
             color_fg= 
               conf['colors']['foreground'] or global_conf['colors']['foreground'],
             color_name= 
               conf['colors']['name'] or global_conf['colors']['heading'],
             color_info= 
               conf['colors']['info'] or global_conf['colors']['text'],
             color_url= 
               conf['colors']['url']['normal'] or global_conf['colors']['url']['normal'],
             color_url_hover= 
               conf['colors']['url']['hover'] or global_conf['colors']['url']['hover'],
             title= 
               conf['title'] or f"{global_conf['title']}".replace("{username}", f"{username}"),
             icon= 
               conf['icon'] or global_conf['icon'],
             name= 
               conf['name'],
             pronouns= 
               conf['pronouns'],
             contacts= 
               conf['contacts'],
             urls= 
               conf['urls'])

if __name__ == '__main__':
    app.run(
      threaded=True,
      port=8080)