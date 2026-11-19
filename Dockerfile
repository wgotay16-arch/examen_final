
FROM odoo:20.0

USER root

COPY ./tienda_unicah /mnt/extra-addons/tienda_unicah

RUN chown -R odoo:odoo /mnt/extra-addons

USER odoo

EXPOSE 8069
