# claude-plugins

Личный маркетплейс плагинов Claude. Сейчас в нём один плагин — **Engineering (Plane)**: плагин Engineering от Anthropic, настроенный под наш Plane.

## Что изменено относительно апстрима

- Трекер задач и инциденты — Plane вместо Linear, Jira, Asana и PagerDuty.
- Задачи раскладываются по двум пространствам по репозиторию: liqu-fi → LIQ (MR, TRM, OPS, DX, HRN, LW), yevaops и yulii/gcs → YEVA (OPP, FW, GCS, OPS). Проект SLU плагин не трогает.
- Затронуты навыки standup, code-review, debug, architecture, deploy-checklist и incident-response, плюс CONNECTORS.md, README и `.mcp.json`.
- Плагин создаёт задачи и меняет статусы только после подтверждения.
- В `plugin.json` нет поля `version`: так claude.ai отслеживает коммиты, и каждый пуш доходит без ручного повышения версии. Версия и коммит апстрима записаны в `upstream.json`.

Все правки живут в `scripts/customize_engineering.py`. Править `plugins/engineering` руками не стоит: следующее обновление из апстрима эти правки затрёт. Меняйте скрипт и перезапускайте обновление.

## Как подключить

В claude.ai или десктопном приложении: **Customize → Plugins → Add → Add marketplace**, ввести `alxwlw/claude-plugins`. Репо приватное, поэтому диалог попросит подключить GitHub и дать Claude GitHub App доступ к этому репо. Затем включить **Sync automatically** и добавить плагин Engineering (Plane).

Если раньше был загружен файл `engineering.plugin` или включён Engineering из каталога, выключите их, чтобы не было двух наборов одинаковых навыков.

## Как подтянуть апстрим

```bash
scripts/update-engineering.sh        # или: scripts/update-engineering.sh <ветка или тег>
git diff                             # посмотреть, что изменилось
git commit -am "engineering: обновить из апстрима" && git push
```

Скрипт берёт свежий `engineering` из `anthropics/knowledge-work-plugins`, заново применяет Plane-правки и записывает коммит апстрима в `upstream.json`. Если апстрим переписал раздел, который мы меняем, скрипт остановится с ошибкой и назовёт файл. Тогда нужно поправить шаблон в `customize_engineering.py` и запустить скрипт снова.
