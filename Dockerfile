
FROM odoo:20.0

USER root

COPY ./tienda_unicah /mnt/extra-addons/tienda_unicah

RUN chown -R odoo:odoo /mnt/extra-addons

USER odoo

EXPOSE 8069

CMD ["odoo", "--http-interface=0.0.0.0", "--http-port=8069", "--workers=0", "--proxy-mode"]

