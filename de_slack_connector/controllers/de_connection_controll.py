# -*- coding: utf-8 -*-
from odoo import http
import requests
from odoo.exceptions import ValidationError
import json
from odoo.http import request


class TokenControll(http.Controller):
    @http.route('/slack_token/', auth='public')
    def connection_auth(self, **kw):
        try:
            if 'code' in kw:
                IrConfigParameter = request.env['ir.config_parameter'].sudo()
                de_client_id = IrConfigParameter.get_param('de_slack_connector.de_sk_client_id')
                de_client_secret = IrConfigParameter.get_param('de_slack_connector.de_sk_client_secret')

                headers = {
                    'Content-Type': "application/x-www-form-urlencoded",
                }
                url = "https://slack.com/api/oauth.v2.access"

                datas = {
                    "code": kw['code'],
                    "client_id": de_client_id,
                    "client_secret": de_client_secret
                }
                de_response = requests.request("POST", url, data=datas, headers=headers)

                if 'authed_user' in json.loads(de_response.text):
                    de_access_token = json.loads(de_response.text)['authed_user']['access_token']
                    request.env['ir.config_parameter'].set_param('de_slack_connector.access_token', de_access_token)
                    return request.render("de_slack_connector.sucess_message")
                else:
                    return request.render("de_slack_connector.failed_message")

            else:
                return request.render("de_slack_connector.failed_message")

        except Exception as e:
            raise ValidationError(str(e))


class EventsHandler(http.Controller):
    @http.route('/slack', auth='public')
    def connection_auth(self, **kw):
        try:
            messages_ids = []
            if 'client_msg_id' in kw:
                de_mail_message = self.env['mail.message'].search(
                    [('client_message_id', '=', kw['client_msg_id'])])
                if not de_mail_message:
                    de_ts = float(kw['ts'])
                    de_date_time = kw.fromtimestamp(de_ts)
                    de_message_creator = self.env['res.users'].search([('de_sk_user_id', '=', de_mail_message['user'])])
                    de_mail_message = self.env['mail.message'].create({
                        'subject': kw['text'],
                        'date': de_date_time,
                        'body': kw['text'],
                        'client_message_id': kw['client_msg_id'],
                        'email_from': de_message_creator.email,
                        'author_id': de_message_creator.partner_id.id,
                        'message_type': 'comment'
                    })
                messages_ids.append(de_mail_message.id)
            elif 'files' in kw:
                for file in kw['files']:
                    de_mail_message = self.env['mail.message'].search(
                        [('client_message_id', '=', file['id'])])

                    if not de_mail_message:
                        de_ts = float(file['timestamp'])
                        de_date_time = kw.fromtimestamp(de_ts)
                        de_message_creator = self.env['res.users'].search(
                            [('de_sk_user_id', '=', file['user'])])
                        de_mail_message = self.env['mail.message'].create({
                            'subject': file['name'],
                            'date': de_date_time,
                            'body': file['url_private_download'],
                            'client_message_id': file['id'],
                            # 'email_from': de_message_creator.email,
                            'author_id': de_message_creator.partner_id.id,
                            'message_type': 'comment'
                        })
                    messages_ids.append(de_mail_message.id)

            # channel in kw
            kw_channel = []
            odoo_channel = self.env['mail.channel'].search([('name', '=', kw_channel['name'])])
            if not odoo_channel:
                self.env['mail.channel'].create({
                    'de_sk_channel_id': kw_channel.get('id'),
                    'name': kw_channel.get('name'),
                    'alias_user_id': self.env.user.id,
                    'is_subscribed': True,
                    'channel_partner_ids': [[6, 0, kw_channel]],
                    'channel_message_ids': [[6, 0, kw_channel]]
                })
            else:
                odoo_channel.write({
                    'de_sk_channel_id': kw_channel.get('id'),
                    'name': kw_channel.get('name'),
                    'alias_user_id': self.env.user.id,
                    'is_subscribed': True,
                    'channel_partner_ids': [[6, 0, kw_channel]],
                    'channel_message_ids': [[6, 0, kw_channel]]
                })
            self.env.cr.commit()
        except Exception as e:
            raise ValidationError(str(e))
