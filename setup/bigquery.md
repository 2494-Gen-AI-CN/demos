# Week 4 set-up: Google BigQuery

Do this at home **before Monday 2 November**. It takes about 20 to 30 minutes, most of it waiting for a download.

In week 4 the ticket desk's data moves out of MySQL and into a **data warehouse**: a database built for answering questions over lots of data rather than for running an app. We use **Google BigQuery**, a warehouse that runs in Google's cloud. Each of you gets your own free BigQuery project, so nobody shares a database and nobody needs a credit card.

When you finish, you will have:

- a Google account
- a BigQuery **sandbox** project (the free tier, with no billing attached)
- the **Google Cloud SDK** installed: the `gcloud` and `bq` commands you type in a terminal
- your laptop logged in to Google from the terminal, so `bq` and, later in the week, your Python code can reach your project

## 1. Google account

Use a personal Google account, for example a Gmail address. Work and school accounts are often blocked from creating projects. If you don't have a personal account, create one at https://accounts.google.com/signup.

## 2. Create your sandbox project

1. Open https://console.cloud.google.com/bigquery and sign in with that account. Accept the terms of service if you are asked.
2. Click the project picker at the top of the page (it may say "Select a project"), then click **New project**.
3. In **Project name**, type `desk-` followed by your first and last name, all lowercase with no spaces. For example: `desk-janedoe`.
4. Look at the **Project ID** shown under the name. That ID is what every command uses, and it can never be changed later. If Google says the ID is taken, click **Edit** and add a few digits (`desk-janedoe7`).
5. **Write your project ID down.** Below, wherever you see `desk-<your id>`, type your ID in its place.
6. Click **Create**, then open https://console.cloud.google.com/bigquery again with your new project selected in the picker.

You should see a **Sandbox** banner. That is correct: it means the project is free and capped (10 GB of storage, 1 TB of queries a month, and tables are deleted automatically after 60 days). That is far more than we need.

If Google offers a free trial or asks for a card, close that offer. You don't need it, and a project without billing is exactly what we want.

## 3. Install the Google Cloud SDK

1. Go to https://cloud.google.com/sdk/docs/install and pick your operating system.
2. **Windows:** download the Google Cloud CLI installer, run it and keep the default options. At the end, leave the boxes ticked and let it finish. It may open a terminal window and ask you to log in; you can close that window, because you'll log in in step 4.
   **macOS:** follow the macOS steps on the same page.
3. **Close every Git Bash window and open a new one** (macOS: a new Terminal window). A terminal that was already open won't find the new commands.
4. Check the install:

   ```bash
   gcloud --version
   ```

   You should see `Google Cloud SDK` followed by a version number and a short list of components (including `bq`).

## 4. Log in from the terminal

Type these one at a time in Git Bash (macOS: Terminal). Put your own project ID in the middle one.

```bash
gcloud auth login
gcloud config set project desk-<your id>
gcloud auth application-default login
```

What each one does:

- `gcloud auth login` opens your browser so you can sign in with your Google account. This lets the `gcloud` and `bq` commands act as you.
- `gcloud config set project desk-<your id>` makes your project the default, so you don't have to name it on every command.
- `gcloud auth application-default login` opens the browser once more. This login is for **programs** rather than commands: from Thursday, your Python code reaches BigQuery through it. On the consent screen, sign in with the same account and **tick every checkbox**.

These logins are saved in a folder in your user profile, not in any project folder, so they never end up in a Git repository. That matters because your repositories are public.

## 5. Test it

Run each command and compare with what you should see:

| Command | You should see |
|---|---|
| `gcloud auth list` | your Google account, with a `*` beside it |
| `gcloud config get-value project` | `desk-<your id>` |
| `bq query --use_legacy_sql=false "SELECT 1 AS ok"` | a small table with one column `ok` and one row `1` |

If `bq` asks you to choose a default project, choose `desk-<your id>`.

All three match? You're done. We'll run the same check together at the start of Monday.

## If something goes wrong

| What you see | What to do |
|---|---|
| `gcloud: command not found` | Close Git Bash and open a new one. If it still fails, run the same commands in PowerShell instead. Your login is shared between terminals, so it only has to work once. |
| You can't create a project, or see "organization policy" | You're signed in with a work or school account. Sign in with a personal Google account and run `gcloud auth login` again. |
| The browser doesn't open after a `login` command | Add `--no-launch-browser` to the end (for example `gcloud auth login --no-launch-browser`), open the link it prints, sign in, and paste the code it gives you back into the terminal. |
| `Access Denied` or `does not have bigquery.jobs.create` | The terminal is using the wrong account or project. Check `gcloud auth list` and `gcloud config get-value project`; fix them with `gcloud config set account <your gmail>` and `gcloud config set project desk-<your id>`. |
| `BigQuery API has not been used in project ... or it is disabled` | Open https://console.cloud.google.com/bigquery with your project selected, then run the test again. |
| A warning about a "quota project" | Run `gcloud auth application-default set-quota-project desk-<your id>`. |
| You unticked a box on the consent screen | Run `gcloud auth application-default login` again and tick every box. |

Still stuck? Post the exact error message in the class channel. Whatever is left gets fixed on Monday.
