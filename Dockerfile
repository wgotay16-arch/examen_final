
FROM odoo:20.0

USER root

COPY ./tienda_unicah /mnt/extra-addons/tienda_unicah

RUN chown -R odoo:odoo /mnt/extra-addons

USER odoo

EXPOSE 8069

ENTRYPOINT []

CMD ["sh", "-c", "exec odoo --db_host=\"$HOST\" --db_port=\"${DB_PORT:-5432}\" --db_user=\"$USER\" --db_password=\"$PASSWORD\" --database=odoo_unicah --http-interface=0.0.0.0 --http-port=8069 --workers=0 --proxy-mode"]


