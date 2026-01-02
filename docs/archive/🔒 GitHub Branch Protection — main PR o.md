🔒 GitHub Branch Protection — main (PR only)

Цель:

❌ запретить прямые push в main
✅ разрешить изменения только через Pull Request
✅ PR проходит CI Guardrails gate

1️⃣ Открываем настройки ветки

Перейди в репозиторий
👉 https://github.com/VictorKVS/devsafe

Нажми Settings

Слева выбери Branches

В разделе Branch protection rules нажми
👉 Add rule

2️⃣ Настройки правила (ВАЖНО — по пунктам)
🔹 Branch name pattern
main

🔹 Protect matching branches — включаем
☑️ Require a pull request before merging

☑️ Require pull request reviews before merging

Required approvals: 1

☑️ Dismiss stale pull request approvals when new commits are pushed

☑️ Require review from Code Owners ❌ (пока не нужно)

🔹 CI / Guardrails enforcement
☑️ Require status checks to pass before merging

☑️ Require branches to be up to date before merging

В списке checks выбери:

✅ Guardrails Enforcement

⚠️ Если чек ещё не появился:

сначала сделай любой PR

GitHub запомнит workflow

потом вернись и отметь

🔹 Запрет прямых push
☑️ Restrict who can push to matching branches

❌ НИКОГО не добавляй

👉 Это и есть режим PR only

🔹 Дополнительно (рекомендую)

☑️ Do not allow bypassing the above settings

☑️ Require linear history (по желанию, но красиво)

3️⃣ Сохраняем правило

Нажми Save changes
(введи пароль GitHub, если спросит)

4️⃣ Проверка (обязательно)
🔴 Попробуй сделать прямой push в main
git commit --allow-empty -m "test direct push"
git push origin main


👉 Должно быть ОТКАЗАНО ❌

🟢 Проверка через PR (правильный путь)
git checkout -b test-branch
git commit --allow-empty -m "test pr flow"
git push origin test-branch


Затем:

открой PR → main

CI должен запуститься

без зелёного CI — merge невозможен

🧠 Архитекторский итог

Теперь у тебя полный governance-контур:

Уровень	Статус
Docs & ADR	✅
Threat model	✅
Guardrails	✅
Tests	✅
CI enforcement	✅
Branch protection	✅

Это означает:

❌ нельзя “тихо сломать” безопасность
❌ нельзя закоммитить в обход CI
✅ каждое изменение — осознанное и проверяемое

Для MVP — очень высокий стандарт.