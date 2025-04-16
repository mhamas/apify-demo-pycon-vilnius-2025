# Apify Demo - PyCon Vilnius 2025

This is a demo Actor used during the [workshop](https://pycon.lt/talks/LAG8AJ) in Vilnius in 2025. It showcases how to implement and monetize a simple Apify Actor using the Beautiful Soup and Crawlee template from Apify. The Actor scrapes the names of speakers at the conference, along with the titles of their talks. The intended use case is to quickly create a database of speakers for potentially connecting with them in the future.

## Step 1 - create Apify Account
Head to [Apify Console](https://console.apify.com/sign-up) and create an account, or login with Google / Github.

![Sign up](images/1_signup.png)

## Step 2 - create a new Actor using template
Head to [Actors > Development](https://console.apify.com/actors/development/my-actors) and cick `Develop new`.

![Develop new Actor](images/2a_develop_new.png)

Click on `View all templates`, find `Crawlee + BeautifulSoup` template, and install it.

![View all templates](images/2b_view_all_templates.png)

![Find template](images/2c_find_template.png)

![Use template](images/2d_use_template.png)

## Step 3 - inspecting the target website
Go to [pycon.lt](https://pycon.lt/) and inspect the pages dedicated for the 3 days of the conference ([Python day](https://pycon.lt/day/python), [Data day](https://pycon.lt/day/data), [AI day](https://pycon.lt/day/ai)).

Let's take Python day for example. Open developer tools in your browser and inspect the HTML structure of the page.

![Inspect Python day](images/3_inspect_page_python_day.png)

Bingo, it seems that all we need to do is to fetch all `<a href="...">` links where `href` is a string that starts with `/2025/talks`. Then, we can get the text in that href (talk title), and find the closest `<span>` afterwards, which contains the speaker name. Let's get to coding.

## Step 4 - coding the MVP
### 4.1 Modifying the input schema
Let's head to `.actor/input_schema.json` and modify the `prefill` for the `start_urls` to `https://pycon.lt/day/python`. While on it, let's also change the `title` of the schema to something more reasonable.

![Modifying input schema](images/4a_modifying_input_schema.png)

### 4.2 Modifying actor.json
In `.actor/actor.json`, let's just quickly change the `name`, `title` and `description` to something more sensible.

![Modifying actor.json](images/4b_modifying_actor_json.png)
