Title: The IndieWeb — Why Your Own Corner of the Internet Still Matters
Date: 2026-09-08
Tags: indieweb, web, privacy, open-web
Slug: the-indieweb
Summary: A look at the IndieWeb movement — what it is, why it exists, and how owning your own site can make you less dependent on platforms that treat you as the product.

## You Don't Own Anything on Social Media

Here's the uncomfortable truth about posting on social platforms: you don't own your content. You don't control who sees it, how long it stays up, or whether the algorithm decides to show it to anyone at all. One policy change, one account suspension, one platform shutdown — and years of your writing, photos, and conversations vanish.

The IndieWeb is a response to that. It's a movement built around a simple idea: **publish on your own domain first, then syndicate outward.** You own the canonical copy. Platforms become mirrors, not homes.

## What Is the IndieWeb?

The IndieWeb (short for "independent web") is a community of people who believe the web works best when individuals control their own online presence. It started around 2010 and has grown into a practical, working set of tools and standards — not just philosophy.

At its core, it's about building your own website that functions as your primary identity and publishing hub, then connecting it to other people's sites using open protocols.

## The Core Principles

The IndieWeb community has codified several principles:

**Own your data.** Your posts, your photos, your check-ins, your bookmarks — they live on a domain you control. You choose the platform, the hosting, the backup strategy. No one can shut it down or delete it from under you.

**Publish on your own site first.** Write the post on your blog. Take the photo and upload it to your gallery. Then, if you want it on Twitter or Mastodon or elsewhere, send it there as a copy. The original stays with you.

**What you put on the web is yours.** It sounds obvious, but most people have never actually exercised this. When you own the domain, you own the URLs, the content, the history.

**Use visible, human-readable data.** The IndieWeb encourages microformats — small, semantic markup additions that let machines understand your content without sacrificing readability. A post is both something a human reads and something a parser can process.

**Build for yourself first.** You don't need to optimize for engagement, virality, or ad revenue. Build something that works for you and your audience, however small.

## How It Actually Works

The IndieWeb isn't theory. It's a stack of real, interoperable standards:

- **Microformats2** — markup that adds semantic meaning to HTML so other sites can understand your posts, events, RSVPs, and more.

- **Webmention** — a protocol for one website to notify another that it's been mentioned. If you write a post linking to someone else's blog and they support Webmention, they get notified automatically. It's like a pingback that actually works.

- **Micropub** — an API for creating and editing posts on your site using external clients. Write in your favorite editor, send it to your site.

- **IndieAuth** — authentication using your own domain as your identity. You log in to services by proving you control your URL.

- **Microsub** — a reader protocol that lets you subscribe to feeds across the web in a unified inbox, decoupling reading from posting.

## Why This Matters Now

We're watching the big platforms rot in real time. Feed algorithms prioritize rage. Shadowbans are opaque. Monetization rules change overnight. The advertising model that funded the "free web" is collapsing, and the platforms are scrambling to extract value from users who've been trained to expect everything for free.

In that environment, having your own site isn't nostalgic — it's strategic. You're building on land you own instead of renting from a landlord who can change the locks.

## Getting Started

You don't need to go full day-one IndieWeb. Start with the basics:

1. **Get a domain.** Something simple, something yours.
2. **Set up a site.** A static site generator (like Pelican, Hugo, or Jekyll) works great. Your own hosted WordPress works too. The point is: you control it.
3. **Start posting.** Write something. Anything. Get in the habit of publishing to your own space.
4. **Add microformats.** Add `h-entry` classes to your posts. It's simpler than it sounds — a few `class` attributes in your templates.
5. **Enable Webmention.** Let other sites tell you when they link to you. Display comments and responses from across the web.
6. **Syndicate outward.** Once your site is the source of truth, use tools to push copies to social platforms. You're now broadcasting, not hosting, on those platforms.

## The Quiet Rebellion

There's something satisfying about it. You wake up one morning and realize you wrote fifty posts last year that nobody "liked" — because there was no like button. You wrote them because you had something to say, and you put it on your own site, and it's still there. No algorithm buried it. No platform decided it didn't fit the narrative.

That's the IndieWeb. It's not a product. It's not a startup. It's just people quietly deciding that the web they want is one they build themselves.

And it's waiting for you to join.
