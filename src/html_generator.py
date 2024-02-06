from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')


class HTMLGenerator:

    def __init__(self, html_source_file):
        self.html_source_file = html_source_file
        self.today = datetime.now().strftime("%A %d %B %Y")
    
    def import_html_email(self):
        with open(self.html_source_file, 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()
        return html_content
    

    def custom_html(self, imported_html, match_list):    
        events_html = []    
        imported_html = imported_html.replace("\n", "")
        today_date = self.today

        for match in match_list:
            match_date = match['date']  # Assurez-vous que cela est au format YYYY-MM-DD
            if match_date == today_date:
                team1 = match['team1']['name']
                team1_flag = match['team1']['flag-url']
                team2 = match['team2']['name']
                team2_flag = match['team2']['flag-url']
                date = match['date'].upper()
                hour = match['hour']
                channel = match['channel']
                game_details_url = match['game-details-url']

                #Paramétrage du style
                font_family = "font-family : system-ui,-apple-system,'Segoe U',Roboto,'Helvetica Neue',Arial,'Noto Sans','Liberation Sans',sans-serif,'Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji';"
                cta_font_style = "font-size: .9em; color: white;"
                cta_color_style = "background: #064534; border-radius: 50px; padding: .7em .2em; width: 100px;margin: 20px auto; "
                team_flag_style = "max-width: 1.5em; margin-right: 3px;"
                line_height = "line-height: .6em"

                match_html = f"""
                            <br />
                            <h3 style="font-size: 1em;">{date}</h3>
                            <div class="matchs-list" style="{line_height}">
                                <div class="match-info">
                                    <h3 class="match-hour" style="text-decoration: underline; font-size: 1em;{font_family}">{hour}</h3>
                                    <p class="teams; {font_family}">
                                        <img src="{team1_flag}" data-src="{team1_flag}" alt="{team1}" class="matchTeam__logo" style="{team_flag_style}"> {team1} - \
                                        <img src="{team2_flag}" data-src="{team2_flag}" alt="{team2}" class="matchTeam__logo" style="{team_flag_style}"> {team2}</p>
                                    <p class="channel; {font_family}">📺 A voir sur {channel}</p>
                                    <p class="cta-infos;" style="{cta_color_style}"><a href="{game_details_url}" style="{font_family}{cta_font_style}">Plus d'info*</a></p>
                                    <p class="source-infos;" style="{font_family}font-style:italic; font-size:.8em">* Source Foot Mercato</p>
                                    <br />
                                </div>
                                <hr />
                            </div>
                            """           
                
                events_html.append(match_html) #On ajoute le match à la liste de tous les matchs du jour

        # html_content_with_events = imported_html.format("\n".join(events_html))
        html_content_with_events = imported_html.replace("{match_details}","\n".join(events_html))
        return html_content_with_events


    def simple_html(self, imported_html):
        imported_html = imported_html.replace("\n", "")
        today_date = self.today        

        #Paramétrage du style
        font_family = "font-family : system-ui,-apple-system,'Segoe U',Roboto,'Helvetica Neue',Arial,'Noto Sans','Liberation Sans',sans-serif,'Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji';"
        
        #corps du mail
        simple_mail_html = f"""
                    <br />
                    <h3 style="font-size: 1em;">{today_date}</h3>
                    <p style="{font_family}"> Pas de match aujourd'hui :(</p>
                    """
        html_content_without_events = imported_html.replace("{match_details}",simple_mail_html)
        return html_content_without_events


    def generate_html_file(self, customized_html):
        with open(f"generated/generated_html_email_{self.today}.html", "w", encoding="utf-8") as html_file:
            html_file.write(customized_html)
            print(f"\nFichier HTML enregistré avec succès --> {html_file.name}")
            return html_file
        