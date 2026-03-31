# Engineering Manager Interview Transcript

> **Outcome:** Zapier declined to move forward after this interview.
> **Job details:** `job-search/Zapier-Sr-Software-Engineer-Partner-Sharing-backend/`
> **Analysis:** See `docs/2025-12-01-zapier-interview-analysis-and-improvements.md`

**Date:** December 1, 2025
**Interview Type:** Job Fit / Behavioral
**Interviewer:** Ryan Bennel (Partner Sharing Team Manager)
**Duration:** ~45 minutes

---

## Interview Transcript

Just... Don't answer it, please. Okay.

Hello. Hello, there. Good morning.

How are you doing? I'm good. Thanks.

How are you? Doing well, doing well. Um, well, cool.

Thanks for meeting with us, and, um, well, me, I should say. And, um, so, uh, let me introduce myself, and then I'll, I'll let you do the same, and then we can jump into this interview process that works for you. Yep, sounds great.

All right, um, I'm Ryan Bennel. I manage our partner sharing team here at Zapir. I've been here about 3 and 3 quarters years, something like that.

3.5 somewhere in there. And, um, uh, I managed several teams here. The partner sharing teams specifically were responsible for all of our partner facing APIs.

We build those, maintain those, and we've got an embed product, like a JavaScript embed that sits on partner websites so they can embed Zapir into their product and things like that. We also own quite a few other little services too, but those are kind of our main things. Um, and, uh, I'm personally based in, uh, it's a time called New Brothels in Texas, and, uh, it's about 45 minutes south of Austin, so, um, and as far as this interview goes, it's not actually for my team.

It's for one of the many teams we have that are hiring right now. So, um, so I'll be taking all everything I've got and kind of handing it off to recruitment in the other managers here. We just kind of end up with a hiring pool here.

So that's kind of how it works. Yeah, that's what I heard. So tell me about yourself.

My name is Brandon Coelo. Sounds like mellow, and I've been developing. It's just been my hobby my whole life, but I went into it professionally in 2010.

I was selling RVs and I decided, you know, career shift into what I, I do for fun, you know, after work. Um, So I've been developing professionally since for 15 years. It started off with WordPress, and then I moved to Lead developer at that company, from scene.

I'm sorry, from senior developer. I ended up hiring more at the company, hiring my boss and some juniors and things like that, moved up to application architect, but I really value being an independent contributor. I don't really want to manage or hire or fire or do these interviews like you're doing all day long.

So I went back to the, you know, IC role and I've been pursuing backend. love automation. I love building systems that stay up, you know, are resilient, our performance. I'm not as much of a style guy.

I'm more in the functional side of things. Been working back in for quite a while. Python Django, mostly with some typescript interspersed in there.

All right. Yeah, I definitely get the, uh, the IC, uh, alignment kind of thing. I was on IC for 15 years, and then I got the itch to go management, and I know a lot of people don't.

Yeah, yeah, yeah. So it's just kind of how it goes. Oh, cool.

Um, well, uh, as far as the format of this interview goes, I just have a bunch of kind of pre-written questions that we ask everybody that are pretty standard, so everybody gets the same questions. And, uh, they do kind of jump around topics a lot. So, one question may not have anything to do with the next one.

Okay. And I'll just work down my list if that works for you. Yep.

Cool. All right, um, can you, uh, tell me about a time where, uh, you were involved in a complex project, uh, that you worked on, you know, what made it challenging? How'd you go about solving those challenges?

The most complex project I've worked on so far just happened last year, and it was a year-long migration, the project was called SDUI, server driven user interface. So all of the logic that was hard coded in Android or iOS. We had a 2 week release cycle.

We had any changes required, at least 2 weeks before they'd get out into the user's hands and that not every user updated. So we were out of sync a lot at headspace. So what we did was we moved all over the logic of what shows on which screens, to which users server side.

So the client side now just gets a fully dehydrated payload of each screen, each section, each button. When they click the button, what's the end point it's supposed to reach out to? If it fails, what's it supposed to do on failure?

You know, all the logic was sent from the server side and the client just kind of had to display it and that cuts down on releasing updates if there's a bug, hot fixes, things like that. So that was a two-part question, actually. I gave you the overview of the project, but you had a 2nd part of that question, right?

Yeah, like what was your process for going about solving those challenges? You know, what technologies did you use? You know, anything like that?

So I was one of the 1st 2 people at the company. What we did was we pulled people from all different teams, people who were kind of agile and adaptable. And I was one of the 1st 2 and initially we did research on our competitors who did this already?

What articles, you know, Netflix, Airbnb, who put out articles on it, and whose did we resonate with the most? And it ended up being Airbnb. They used a sections and screens set up with kind of like an object where you have which screens and which sections all come together so that you can use one section on multiple screens if you wanted.

It kind of saves the response size. We had an existing API endpoint already serving responses to the client side, so we didn't have to set up a new endpoint. But it was only doing about 10% of what it does now.

It was real small niche in point, and we added new endpoints to that backend service, and we expanded it using the current system, which was typescript happy API system. Uh, so technical challenges from the beginning were just how granular do we break down these screens and buttons and, you know, do we do colors? Where do the images live?

Do they live on the server or do we send them back? Do they keep them in the client side so they're there for every release in case, you know, the web's down? We can use it in the background.

I might be getting off track, but I wanted to give you an idea of the project. Yeah, I mean, as much detail as you want to share is good. Um, so in in spinning up and developing this project, um, who did you collaborate with in, uh, you know, cross-functionally, cross teams, or things like that?

What did the collaboration look like? So, I, when I came to headspace, I was on a team. I'm sure Zappier has done it too, where you might buy out a company that has a technology that you want and you need to integrate that into your company.

I came in kind of on the secondary team at headspace. So our team was smaller and the larger headspace team was more established and they'd been there for a while. When I 1st started, I said I was one of two.

The 2nd was a principal engineer that was at the headspace side for already for 5 years or so. So they knew their system well. And I knew the system that we were going to be merging with theirs.

So initially it was just us two. I'd never met her before. We collaborated in Slack, Async.

We had meetings twice a week, just to catch up and see what needed to be shared. When the team started expanding, we had a manager come in from a different team. And I can't just say that we worked with one other team because it was literally each subteam of this project was made up of different people from the company.

So it was like, I guess, cross department, cross team, everybody was new working together. But we did it through daily stand-ups, both Async, daily stand-ups, and Slack, and then team wide ones where we would raise any kind of roadblocks or we call them parking lot issues where at the end of the conversation we could talk about what's remaining. We've got lefto.

Yeah, you know, you manage them. So it was, it was ran like a normal agile system, but all the team members were kind of put together and picked from various teams. So as far as, like, requirements and, you know, products of desire and things like that, who did you end up communicating with just to, um, get requirements, get questions answered as far as, like, uh, you know, if you, there was a requirement that wasn't clear or something.

Yeah, this was one of those startup type projects where it was there was no real project manager on the team. We had guidance. We knew what we were building, but we had a tight deadline and we were really efficient.

We had a new CEO and he's like, just move fast and break things. We need to get this done. So there was no mock-ups.

I had a lot of questions. I'm very meticulous. So I didn't I needed to have answers before I put something out there, especially if it's something on the headspace side, which I had never touched before.

I would go to the staff and senior, not staff and principal level engineers who had been there for 3 or years or more. I would go to them with all of my questions, and if they couldn't answer it or they didn't get back to me, I'd go to my manager, and I'd let them know, hey, I reached out to A and B. Hadn't heard back in a day. Do you have someone else or can you answer this for me?

It was really that. The senior level engineers and above and the managers were my fallback. All righty.

Were you all successful in building what you were setting out to? You have opened the results of the? We released on time, a functional, there was about 3 screens.

The onboarding, the profile, and I forget the last one, but we did hit our goal of releasing it was June, the end of June this year. There's always fast follows and improvements that are still going out now, but as far as technically, we did release on time. Cool, yeah.

Awesome. Great. Just at one side note, I forgot to mention, I'm gonna leave you about 15 minutes at the end of this, just to ask whatever you want.

Okay. I meant meant to say that in my intro, I totally forgot to. No problem.

Um, so, uh, cool, thank you for the the answer to that one. Next one here is totally unrelated. And it's a couple AI related questions.

So how do you see AI evolving the role of an engineer, software engineer in the next 3 to 5 years? And how are you personally preparing for that? I don't know if I said it in my answers previously, but I'm a very strategic person.

I got tested at one of my early jobs. We went to Gallup Strength Finders, which is owned by, I forget, but it was, it's a $1000000000 company. They test your professional strengths and strategy was my number one.

So I've been chatting with AI for about a year now. AI is going to replace my job. I wanna retire in, you know, 15 years or so.

What can I do to make sure that I still have a job in 5 years and 10 years when AI is doing everyone's work? Who's going to be there to control the AI? What are those job titles called?

How do I get there? So I've been really thinking ahead about this. to the point where I've never really done infrastructure much, really heavy back end. I can do anything with infrastructure as far as docker, you know, uptime reports, logging, error correction, things like that.

But it's never been a title in my job before. I'm using AI daily to plan code for me, audit code that I've written. I like to have it spit out code, but then I will critique it and, you know, iterate on it and fix it.

So I'm using it in every step, personal and professional. I use it for planning Thanksgiving dinner, you know, give me a timing sheet. Here's all the different things.

Here's when they need to start, you know, cook them at the same time. Don't do them one at a time. You know, I, I have a slash command slot up and clawed code.

I have agents. I, you know, everything you can imagine. I've been doing it.

In 2019, I took a full year to study machine learning, which is kind of what it was called at that time with reinforcement learning. It's kind of like you let it play video game over and over till it finds the absolute fastest way to beat it, and one you may never have thought of. So it's just a passion that I've I've had forever. been using ChatGPT since 2022.

Cool. Very cool. Yeah, I did notice on the application that you filled out, you sound like you've been using AI for quite a long time, longer than most, I would say.

Yeah, yeah, it's, it's the, you know, coding was always my thing. Computers was always my thing, but once AI came out, I'm like, this is like a game changer. I love automation.

I love just setting up systems and AI just makes so much of that so much easier. Yeah. Cool.

Can you tell me about a time where you had a, um, an AI coding tool that you used to help you solve a problem? And, you know, what made you decide to use AI for it? I guess so, what made you decide you've kind of already talked about your motivations and that, but...

Uh, yeah, so... Domain names are like business names. The earlier you get in, the, Let me just skip the story part and tell you, I have an old contact who controls special needs.com.

And with that kind of domain name, you don't need to do a lot of marketing. I mean, if you just have some a special needs.com blog, you're going to get traffic just eventually. So about 3 years ago, I decided to completely rebuild it from the WordPress website that it was to be a react next GS front end with a Django back end with Cloud Flare workers as a caching layer in the middle.

I used AI every step of the way. The biggest, though, was I created, I think, 70 virtual authors, each with their own voice and, you know, writing topic with their experts in, in the special needs niche. I would have, um, what's it?

Ling Chain models and structures. So the content that it was generated followed, you know, very rigid guidelines for the generated content, HTML versus marked down. It would verify it when it was done.

And this was all done through APIs. There was no like clawed code or connections at the time. It was just API calls.

I even had Google, I had 4 different API providers that it would run through the free 11st, and then it would quality check the answer, and then it would run to the next cheapest one and quality check the answer until it got an answer with a quality score over, you know, 80% or something, and it would use that one. So I just used AI for that entire project. Cool, awesome.

So, how do you can go about staying up to date on what the latest AI stuff is, latest day? news, the news models, you know, all those kinds. Um, mostly the 2 sources would be YouTube and Reddit. and subscribe to quite a few subreddits, and I do AI related searches on YouTube for tutorials and things, so then I, there's always the weekly updates about what's new when you visit places like that.

All right, well, great. I'll move on to my next question here. Um, can you, uh, tell me about a time you were involved in responding to some kind of incident, uh, like, an outage or maybe a critical bug was discovered or something, but like that, and what you did?

This was my, uh, most proud one, but it was a long time ago, still stands out, though. We had a word press WordPress website where after 5 or 6 hours of being deployed, it would randomly start hanging. Resources would start hanging.

We could never figure out why because it didn't matter if the deployment was a single text file change or something database related or not. There was no connections. I don't, I don't remember at this point what led me to finding the solution, but I can, I do remember the bug and the solution.

It was a core PHP logic bug that was known and reported. So it wasn't anything in our WordPress or our stack. It was like an actual core PHP memory leak where after 10,000, like files were added to this memory, it would just, it wouldn't clear them out and it would just kind of freeze and lock everything up.

So nothing else could be written to it, and that was causing cascading problems. So there was some GitHub issues with potential solutions in there. We tried a couple of them, and when one of them stuck, we deployed that.

Thanks. What, um, as far as your, your problem solving, you know, getting through that, how did you go about it even finding that it was related to, like, core PHP functionality? Yeah, at the time, there was no AI assistance, I would have gone right to AI, but it was...

I think looking at, on the whole disk, the most recently modified files, searching everywhere, what was touched right before it started freezing, and that led us to some of the core PHP, um, PHPFPM files. So once we got into the core files, we knew which file was being touched last. That's what we took to our searches.

And that's what ultimately led us to finding the issue we were having. Gotcha. Was it was it just a out of curiosity?

I actually kind of started my development career with PhP as well. So, um, was it, um, was it like bike code cashing or something that was, it would hit some kind of limit? I didn't, I didn't ever hear of that, but...

Yeah, that soon as you said bike code, my light bulb, an old rusty light bulb went off in the back of my brain, says, that sounds right. That could be it, but this was probably 2017. So I don't remember the exact what type of issue it was.

Gotcha. Do you know if they ever eventually, like, fully resolved the issue? Like the PHP community?

came out with a new version or whatever. Yeah. No, we did check pretty regularly for some something like 4 or 5 months, we would check every week for an update and then I think it just fell off our radar.

Oh, okay. Got you. Cool.

All right. Um, can you, could you tell me about a time where you worked on a project that wasn't clearly defined, and, uh, how you make progress with it? Yeah, um, I already gave you the, the big one, which was the server driven user interface, um, but aside from that, when I was at the penny hoarder, I was walking to lunch with my boss and he mentioned a project that was coming down the pipeline called a work from home jobs portal.

We we connected to a 3rd party zip recruiter, API, and we would pull in jobs every day and we wanted to list them on a searchable portal on our site, but there was no planning for it yet. It was just a, hey, we're discussing this. And I told my boss, yeah, I'd like that.

That sounds interesting. And I got to be on that project as the lead. What we ended up doing, well, before I get into implementation and how I went about that, you didn't ask about implementation, right?

What was your question for this? These are the questions I think are pretty open-ended. So anything you want to talk about, you know, how you made the decisions on what you, you know, your tech stack or anything like that.

I'm always interested in that kind of stuff, so. Well, at the time, our WordPress website, the admin screen, was going through some pretty heavy performance issues where I think if you saved a post, it would take 30 to 45 seconds in order to save it before it would reload the page and show you your content was saved. I didn't want native WordPress work from home jobs portal.

That was a bit almost like a new content type. It was a bit, uh, Too integrated under the word press and verbose. I wanted something that was kind of modular that we could put in there as a trial and rip out if we don't want it later.

So I ended up using a single page application framework with a react front end with web sockets connecting to the database and WordPress API on the back end, not API. It was a web socket, but we would have a search box on top where as soon as they start typing, it would query the back end instantly. And I think it was like, sub 50 millisecond responses they were getting for jobs as they typed, which I really liked.

It was my 1st kind of single page application. If they clicked on a listing, of course, it just kind of loaded on the screen form. They didn't have to change the URL or wait for the page to load and I learned all about, um, I was using Sprites back then where you could separate one large image into smaller sections and load it from, you know, 10 pixels over and 10 pistols down.

It went really well and we kept it just like it was the whole time I was there. We didn't actually move it to WordPress-based, uh, I guess, powered back ends. We left it with the web socket and react because it was so much more, I guess, performant than changing it back to a asynchronous page load, or a synchronous page load, sorry.

Cool. So, along the way, as you were kind of making decisions, um, what was your your methodology for documenting those decisions and sharing any decisions you made since the, you know, the requirements are a little fuzzy at first? I first...

I was the only one on the team during the this planning phase. I came to my boss and I said, I was thinking of doing this. We just, you know, when he was sitting next to me.

And he was okay, go ahead. and that sounds good. So then I did research on using a web socket versus the WordPress WPJSon endpoint on REACT versus native JavaScript or JQuery, because WordPress had JQuery. If we should use an eye frame to hold all this in the middle of WordPress or if we should extract the header and footer from our theme and like make this a standalone site.

I did all of my initial thought, what I would do if I were designing it without any other input, is what I put together 1st. And then at the penny hoarder, which is where this was for, we had a teaching Tuesdays where we could get together and talk as a group about projects we've done after we released them. What decisions did you have to make?

What would you do different? What research did you do along the way? But I kind of took one of those sessions and used it to get feedback from the team before we actually started this project.

And that's where we kind of got some of the web socket. Discussions versus API. That was a big one.

But yeah, that's how we started it. It was brought to me. I came up with an initial design, brought it to the team, and we refined it before we started working on it.

So, in hindsight, is there anything that you wish you would have done different or that you would do differently now? based on what you know now? Yeah, I, there was a phase.

The web sockets were probably nice, but not needed. You know, if you have a fast stable API endpoint, you can get similar response times. I just, We weren't sending any data to the browser, so we didn't kind of need that 2 way communication.

We just needed to say, give me this job listing, here you go. Here's that job listing. So probably should have used an API endpoint versus a web socket.

I just really like having, um, at the time, I liked web sockets a lot, so that's what we did. Yeah. Yeah, I can go either way on that one too.

I think. There's something cool about keeping that open socket that you just... I like to be able to push notifications to them if I can, you know?

Like, the little counter in the corner goes up in real time instead of on a refresh. It's just nice. Yeah, yeah.

Cool. All right. I'll jump to my next one here.

Can you tell me about a, uh, time when a product manager or some kind of stakeholder or teammate or someone? made a case for a feature or of the way to implement a feature? It was like a teammate or something, and you disagreed with it, you pushed back and said, hey, let's do it a different way.

Something like that. Yeah, when I was working on the WordPress website, we had a newer dev ops person. It was the only Dev Ops in the company.

We didn't have that position before. And when they came in, they wanted to dockerize everything, which I hadn't done before. And that was fine.

I, they did. They put it in docker, and I thought, this is great. We all use docker now.

Been using it. almost 10 years now. But a few months after we had our docker stabilized, he wanted to go to Kubernetti's and have a swarm. Our website was almost like a blog.

It's financial advice website. We didn't have high performance needs or, you know, we didn't need that redundancy. And it was something that we went back and forth a bit, and ultimately my boss did tell him, like, it's okay.

You can, you know, you can do this. Try it, give us a proof of concept. Uh, we...

Never really got it up and running though. There was problems with. There was a tool.

You know how there's terraform for infrastructure? There was a coding tool, their language he was trying to use with Kubernetti's on top of it that he just couldn't quite nail down. And the deployments were never turning green, so to speak.

So it didn't end up going out, but I had my reservations about why we needed something like that when we have a WordPress website with our database is already like on Amazon, they switched over to a server list database back then. RDS was serverless, so we didn't have to worry about the load on our database, and our WordPress site was so well cached that I just didn't see the need for spreading us out over 3 or 4 servers at that time. Cool.

Um, so what ultimately was the outcome? Did it just kind of not go anywhere or... We just kept it dockerized.

Yeah, the Kubernettis never took off. It was, I don't want to say a failed experiment, but he just couldn't nail it down. so to speak. So we never got it working.

Yeah, that's cool. potentially a classic case of a little bit of over-engineering maybe. Yeah, yeah, that's what I was thinking. Um, so can you, can you tell me about a time that you had to, uh, solve a technical problem, uh, using either a tool or technology that is brand new to you?

Um, you know, how did you decide on that tool? What made you have to use that tool if it was something that was forced? You know, what tradeoffs did you consider?

Things like that. Hmm. Well, with AI, I mean, this question is going to be outdated pretty soon because so I had I had a job interview recently, not recently, but you know, less than a month ago, with a company that it was weird because they said this is kind of like, we want to see how well you use AI.

So you have to use cloud code for this interview only, cloud code, and record, here's the 1st prompt to give it, which tells you to record everything you do. Every prompt I give it, it writes it to a file. But you're to create this feature request system where users can upvote requested features.

So it needs to be native iOS, and I've never touched any kind of native iOS code, and it was timed. It was a 2.5 hour interview. I actually had to install Xcode and download it with like 10 gigs or something.

It took, took a long time for it to download and install and configure. So while it was doing that, I was going over the instructions with cloud code and planning, okay, the front end's going to be this uh, native iOS front end. The back end's gonna be Django.

We don't need to worry about tests yet, but we need to make sure that when they, you know, this and that, I don't need to get into it too deep, but it was completely new for me to integrate a native iOS app with a Jingo back end and package it up. Releasable light. The limit was 2 hours.

I got it done in 2.5 hours and I did move through all the rounds of the interviews, but then they ghosted me recently. Yeah. But that's the most recent example of being required to use a technology or framework or language that I knew nothing about and how I accomplished it.

It did get done. There was no real style to it. It was all default styling, but it was working.

So that's an interesting challenge. Yeah, I've done, I don't know if you've ever heard of Zamarin, but it was like a multi-platform mobile app development where you could, you actually write it in C sharp or, you know, it's done by Microsoft. But it would compile to iOS, Android, and at the time, wind phone was a long time ago.

Yeah, because, uh, never, never done it natively for iOS. Kind of an interesting challenge. Yeah.

I mean, cool. So, um, kind of a topic shift here a little bit. How do you decide, uh, when to build, you know, when's the right time just to build a quick prototype, uh, versus, um, building a long lasting product that that is actually going to be the final, uh, thing that gets implemented, um, you know, at least the start of it.

And, you know, what are the risks and things that you consider there? It depends on where the product idea came from, if it's something like, me or one of my teammates suggested to our manager or just in the broader slack, hey, what if we had this feature on our website? And if there's agreement, yeah, that sounds good.

That's when I think you do the, you know, the weekend work or, you know, the Friday, sometimes you get a couple hours on Friday where you can work on something like that at certain jobs. That's where you do a small POC basically. Just can this actually integrate on our system and what would it look like, I think?

But if it's something that's business driven, product driven, we're getting a lot of complaints that our API results aren't searchable. You know, we need the customers would like to be able to have a search endpoint versus reaching out with the exact ID that they need. That kind of thing is sounds, just even at 1st glance, like it's gonna be a more long-term project.

You need to integrate it properly, even if you're doing a POC, you need to integrate that POC as though it's going to be released because it most likely will be. And you're going to be touching a lot of things that are already existing. So removing it back out of the system can be complex or you might leave some traces of it if you decide not to use it.

So I think when it has like a clear business need or it comes from like the CEO or clients directly, you should put more effort in a POC versus maybe something that's not user facing, like the admin screen, if you want to add a new feature to the admin screen that might just improve the developers' lives, but not necessarily reach the client, doesn't make any money. Um, those are ones where you can probably spin up something a little. I don't want to say shortsighted or simple, but without as much planning with the integration.

If it works well, then you can refactor later, I think. Cool. Um, so, so how would you go about, um, deciding when you should resolve tech to potentially, you know, left over from an early POC or something like that?

You know, what, when do you think is the right time to address it? Ideally, um, soon as you know it's, it's debt, you need to record it somewhere, even if you just make tickets and in the backlog, um, like, Imagine, we say that. If you have a feature, call it a survey system built into your app and you no longer use that survey system, but it's wired into 18 different files.

That kind of tech debt can't be removed in one day sometimes. It might take a couple weeks or a quarter to refactor everything to completely remove it. So you always need to record your tech debt and make sure you're aware of it.

The things that may seem higher priority if that tech debt is causing slower development time or performance issues. You should address it right away. If it's actually impacting your team.

If it's taking up space on the server, but it's not impacting anything yet, I think it's important to document it, but those. That's more of a managerial type decision, but how often do you go through the backlog and prioritize these things maybe once a quarter as a team and you say this one should be moved up, it's been there for too long. Um, I would leave the more low hanging, I'm sorry, the less important ones to those quarterly reviews and the more important cost driving ones should probably be handled in every sprint that we get one ticket from the backlog or, you know, the the work that needs to be done for us.

I can keep the lights on, is another term for it. We get one ticket from that each sprint just to make sure that it gets done. But the bigger ones should probably be planned out.

I'm getting a little off track here, but That's it. Awesome, thanks. Um, uh, next one I've got here is, can you tell me about, uh, learning from a mistake that you made recently, if you have one, or, you know, more in the past, if you don't, um, that kind of impacts how you, how you do your work.

Some kind of mistake that, you know, made an impact on me. Yeah, it's not recent, but it has affected everything I've done since then, and I still do today, so I wanted to, I always use this one as my example. When I was at the penny hoarder, which is the company with WordPress, HTTPS was not required by all browsers.

It was still like, you should do this. It's best practice, but not every website does that. Well, we were converting to HDPS and during one of the releases, there was an intermittent problem where the whole site was down, but only on certain devices, that certain, and it was only after a certain amount of time that it would go down.

It, it, turned out that there was a certain iOS version that was generating a cache that was then cashed and served to every device. And that cash was using insecure links for like the CSS and things. So the page would load without any CSS.

It, it was, I was the driver on that, and it was a, not cloud flair. It was a cloud front caching issue in the end based on agent, user agents, things like that. The site was down for probably about 6 hours intermittently one day, which was a lot for company.

I was really down on myself and apologizing and slack to all the chance. Sorry about this. Sorry, and all the writers and all the people from other teams were like, we understand you're doing great.

That's fine, but the boss called me that night and he's like, I'm here to tell you that it's not okay. you know that was a big deal. Um, and it just turned my gut upside down to get that call from my my boss that's saying it wasn't okay when everyone else was saying it was. I appreciated his candor and directness, and I just double check everything I do more now than ever because I don't want to be in that position again.

Yeah. Yeah, sometimes that candid feedback is really valuable and people, I think, a lot of times are afraid to give it. Yeah, often more afraid to give it than they are to receive it.

Yeah, I know. I was happy he gave it to me, but I also like, it was a big gut check moment. Yeah, yeah.

Sounds like a good learning opportunity there. Um, all right. Could you tell me about a time that you received some kind of technical feedback?

It could have been in, like, a PR or MR or something like that or, you know, some implementation spec you came up with or something like that. And you disagreed with the feedback you got, and how you responded. Yeah, I'll...

I don't know if I have a... Honestly, I can't think of an exact one issue that stands out, but I do know of like a theme that would happen a lot with different PRs. Because we would have different teams reviewing the PRs, we would get different reviewers and every PR reviewer, like some just sign off, some get real nitpicky, you know, and some will be anywhere in between.

The comments or issues that I might get would be surrounding areas of the application that I hadn't touched before. And I may have been doing it suboptimally, um, some, not reinventing the wheel, but maybe there's already a function doing some of what I want or maybe I was making 3 database reads when I could have combined them into a single read if I had known about this other model in the system. So I, I've gotten a lot of feedback about, why are you doing it this way?

Did you know about this feature over here? And that's kind of all it is. They don't tell me which one to use.

They just point out that there's something else that may be doing it already and I I love that. I want that because when systems get so large and you have, I think there was 500 engineers at headspace or something like that at one point, so many that nobody knows the 10 year old system all the way through. So you never learn about these things unless someone's willing to point them out to you and show you what you can do better.

That's, you hadn't asked about mentoring, you might ask about mentoring eventually, but that's that's what I think a good mentor is, is saying, I see a problem where this could be better. And I'll show them kind of what we've seen this before. Here's how we solved for it.

And this is probably what you should do going forward instead of recreating it. Use what we already have. I like that.

Even if it's, um, naming conventions, if I'm too vague with a variable name or something, and we have standards that I didn't know about, and if they share the standard stock with me, I can at least read it over and, um, incorporate into my AI rules, but also look at it myself. Awesome. So, um, little off script here, I was curious, um, uh, I guess in your your resume here, you mentioned like Django work and things like that.

Can you, uh, tell me like an example of something that you've, you know, project you worked on in, um, in Django, uh, you know, specifically if it involved, uh, either writing or, um, well, if, if you work directly with APIs, like, that'd be great too, but, you know, what's an example of, um, uh, some Django work that you did? Let's, that's everything I've been doing the last 3 plus years. It's been Django at Headspace, existing endpoints for the most part.

I have created some new endpoints and we have views that handle those, um, All of those have models. So, at headspace, it was already set up. It's all endpoints that have Views and models associated with serializers and signals that when something's saved to the database, it runs X, Y, Z. But setting up my own, on my own, the special needs project was one where it was green Greenfield work.

There was no Django or no Python for special needs at all. So I set up a brand new Django app with sub apps for articles or listings or users, contact pages, anything you would need for a site. There was a different Django app set up for it, and each one has models in their own serializers, and again, and signals, and multi-step validation when data comes in to make sure it's secure, and jot tokens for users, authentication, role-based access, it, everything, um, that you need kind of for a Yelp style website is what I built in Django for the back end for that.

Okay, cool. Um, as far as like, um, scaling and, you know, uptime reliability, monitoring, and things like that, um, you know, what what scale were these systems out? Are they really, uh, high traffic and, you know, how do you how do you monitor if things are, um, going wrong?

Most of the time at most companies, I think nowadays there's teams that monitor that more than the engineers. Like, I'm a Django engineer, so I'm not as much in the performance or the server up time side of things. We have teammates for that.

But what we did do is we made sure that we had decorators that would, we could just put above a class or a method in a class that would log the timing to rapid 7 or new relic. We'd use new relic a lot for this. Just adding the performance, monitoring tools into the code that we create.

And checking after release of something that, say, has a database impact to make sure the database queries, there's no spikes or anything out of normal for the few hours after release is typically what we would do, make sure we're recording it, monitor once released, but then we don't look at those charts again probably until there's some kind of problem. Okay, cool. Um, and as far as, um, typescripts, I think you had mentioned typescript at some and, uh, yeah, it was like the uh, the SDUI project.

Um, you know, what experience do you have in typescript and, you know, you don't have to go into a lot of detail, just more looking, like at a high level, how much typescript have you worked with across, you know, your career and recently? Typescript itself, I only really started picking it up. It was June of 2024-ish.

That's when we started the project and it was a year-long project. I had, I don't even remember where I touched it before, but I had used typescript only once or twice before, and I think that was because it was already in typescript and I had to extend the project. I've been using JavaScript forever.

That was and even react. I've done a lot in reacts, but typescript itself was new to me. So, I have about one year of experience.

That's that year on that project, and I learned all about the interfaces and typing and lazy or what's the word? I'm not lazy, but when you can cast things as any, instead of doing it the right way, it's like shortcuts that, sure, they get the compiler to be okay with it, but you're just ignoring all the features of typescript, all the features that make it safe. So that was my biggest stuff when I got poll request feedback.

It was like, you shouldn't use as any or as unknown. You should create the interface or whatever, so it knows what to expect first. But I would still say I'm mid-level to beginner, you know, in typescript.

Yeah, I'm purely asking because I know one of the teams at hiring, they, their code base that they work in is very, very JavaScript heavy, and they recently, within the last year or 2, started converting to typescripts. So, yeah. I'm asking just, because, you know, for whoever looks at this going forward, so.

Yeah. Cool. All right, well, looks like we've got a little less than 15 minutes left if you want to ask any questions about, um, Zappier, uh, various teams, myself, um, you know, anything like that.

Yeah, I, so what drew me to Zappier was the one AI, I'm sorry. Yeah, AI, but also API and automations, and it's just kind of a melting pot of all the things that I'm interested in, but remote 1st is something you guys have kind of talked about. What's that actually look like in a, as far as work-life balance goes, is there like on call on certain teams or are there certain, for example, is there an infrastructure team that handles all of the after hours issues or are engineers that would be in my position also in on-call rotations?

Um, What about any kind of annual get together? Just a remote culture and work-life balance. I'm curious about.

Um, so, the teams are pretty hands-on with the stuff they work with. So on-call, there is almost every team has an on-call person on rotation. What I will say is it's very, very rare that, you know, you get woken up in the middle of the night over something, like, it might happen once a year, and it might not even happen that often.

What on-call typically looks like is if, uh, some kind of emergent issues or, you know, somebody from another team or from the outside and is a customer that needs urgent support, you, you may be the one who ends up working on that. It varies a little from team to team. Um, but uh, if there is an incident of some kind, you're, you usually take point on that.

But, uh, it's, it's, in my experience, over 3.5 years, it's, I don't know, maybe twice, I've seen, you know, some alarm bell went off at, you know, 3 in the morning or something, and someone have to get up. It's pretty rare. Um, as far as the, uh, work life balance and things like that, I think Zapir really has it nailed, uh, pretty well.

Um, developers can uh, typically, you know, within reason, set their own schedule. If you need to take off in the middle of the day for an appointment, you just change your little slack status that you're in FKAK and, you know, come back when you're right. Um, uh, and, uh, we have, um, as far as, like, we're all some flavor of agile.

Every team can kind of pick their own, you know, flavor. Some are very combine heavy, so it's, you know, there's not sprints, but, um, you know, uh, as far as that kind of stuff goes, there we pretty much every team does some kind of a daily stand-up, but it's asynchronous. So you'll get a thing from a pop and slack or there's a channel that, uh, you're supposed to go into and every team kind of separates or implements that the way they want to as well.

Teams could have a lot of control over the specifics of those kinds of things. So, um, So you go in and do that. Every team has, it's kind of mandated.

You have to have, uh, um, a weekly team meeting, which is a good thing to mandate, get everybody, uh, face to face over Zoom, at least once a week. Um, my team, uh, we have sprint retros and sprint plannings. And, uh, we personally, you know, on our team, we do 2 week sprints, so we do all of the retro and the planning within a 2 hour window.

Um, and so it's not like an all day affair or anything like that. We just, and it usually takes an hour to do both. So it's, it works pretty well, but those are over Zoom.

Uh, we do have a yearly, um, meetup, uh, summit they call it, and, um, that's where everybody in the company, worldwide, is invited to come to wherever they set it, uh, this year. It's gonna be in LA, but it's been in Austin and New Orleans, Denver, since I've started, and then a bunch of other places in the past. And then everybody gets together for a week.

Um, kind of do two days of really company specific stuff, and then the rest of the team is the rest of the weakest team related stuff, uh, and a free day, free day and a half. to kind of do things with your team. So, um, And, uh, and every team kind of has their own culture a little bit because, uh, the, there, there's usually around 5 or 6 developers, uh, sometimes 4, it varies a little bit. And then engineering manager, and a product person who's assigned to the team.

And if the team has a UI component, which not all teams do, they have a designer assigned to the team as well. Oh, that's right. Your company... primarily connections and content.

I mean, I know there's like, uh, you gotta, if state, I forget what you call it, but there's like the if statements, so the connectors that can fire off, but you don't have a whole lot of client side changes all the time, probably, compared to the back end. There, there, we have like the editor team and they, they make changes to like this app editor and and so that's, you know, they make quite a few changes. a pretty rapidly evolving thing. But, you know, not all our teams, like, my team is, we will bring in a designer if we need to mess with our embed.

But our embed kind of lives. and it doesn't get touched very much. So most of our work is very back end centric. So we'll borrow it, uh, a front end developer from another team for a month if we need to make some changes, something like that.

This sounds, the work environment you describe sounds similar to headspace, but it's, it sounds great. I'm an early riser. I have 2 kids.

I'm single dad, so I have 2 kids full time. And they're homeschooled. I dont need to homeschool them during the day.

They're old enough now where they kind of got their own classes and things, but I do need to, um, sometimes in the afternoon taking places, you know, sportings in class and I like to have a, uh, this all being said, I usually work earlier. I'm on the east coast and even then I like to work early hours and get some things done before they're up before the east coast is up. Um, And the style of that you mentioned with the meetings, um, would work great for that.

Yeah, that's great. We trying, like, any meetings as well? Like, it varies team to team, but like, I put our meetings around noon or one.

Central, which means that pretty much everybody in the US can kind of overlap somewhere in there. Yeah. Yeah, that's what I was wondering.

Usually there's a bit of overlap for East Coast, West Coast, and sometimes beyond, you know, Brazil and England, things like that. Yeah, I don't, let's see, it's a few minutes left. This is the fit, the small team, you said, which sounds interesting, manager.

One product person. Um, How do you guys go about training, mentoring, helping each other out on these teams to kind of lift up the ones that need a little more support, I guess, um, than new people or lower level? Um, yeah, so as far as, uh, you know, lower level people go, we have a coaching program, uh, internally that anybody can sign up for.

You can sign up to get yourself a coach and then there's people who volunteer to be coaches and you can you can get that. But there's also a pretty heavy, um, culture of just general mentorship and things like that, especially we don't, you know, especially with AI and the way that AI has kind of taken over everything, we don't have as many juniors anymore, which is really like, I think, what everybody saw coming immediately. Yeah.

We don't hire many, like, level ones or twos anymore. It's not that it doesn't happen, but it is kind of rare. So mentorship is more of, I think, uh, The way that I've seen it evolve into is more of, you know, your seniors kind of, you know, will give more practical advice and and help to, uh, the mid-level people.

And the way that those work, L1 is like super junior, brand new entry level almost, maybe a little bit after that. L2 is kind of like advancing toward mid-level. L3 is considered mid-level and L4 is considered senior.

So if I use those terms. So your L4s will kind of work alongside the L3s, and if an L3 is leading a project, kind of as an experience thing, and L4 will kind of be hands on with them. Um, uh, you know, looking over everything they do, make sure it's good, give advice.

Um, a lot of MRPR feedback, but whatever you call it, uh, uh, things like that. So, uh, yeah, mentorship is definitely very, um, encouraged and, uh, typically people want to advance. And, uh, um, so they're actively looking for that kind of mentorship, too.

Yeah, I like to help when I can. Once I know a system well enough, um, I like to give back and help the lowers. I just, I don't like leading big, um, company wide, you know, training sessions.

So that's why I was asking, wanted to make sure I didn't have to lead training sessions for 50 people sometimes. No, nothing like that. But, you know, on my team, for instance, if you had something you wanted the whole team to know about in the demo retro meeting, that's something where you could like say, hey, let me show you guys this thing I've discovered or whatever, but, uh, Yeah, I'll often record a quick 32nd to 2 minute video and put it in Slack and be like, watch this back and fast forward.

Don't watch it. I don't care, but here's here's what I was thinking about this this topic, um, just more async. Yeah.

Yeah, as far as, like, uh, for your 1st question, though, the work-life balance, especially, like, my daughter's homeschooled, and, uh, and, and so it's similar where, you know, it's very, uh, flexible. Yeah, that's that's it. We don't have the same schedule every day.

You know, sometimes it's a cooking class on Tuesdays at 2 o'clock, you know, that's not always planned either. So that's good to know. Yeah, you see in people's calendars, everybody's calendari and the company's public, and so you often see in there, like, somebody puts an event that's very related to something their kid is doing. something like that, where they just step out for a while.

So, like, I want to be, uh, useful with my last, it looks like 2 minutes here now. I really do like everything I've heard about this company, and I know this job market is really hard to get hired. So I guess what advice do you have to help me through the rest of the rounds?

What's important to you guys that I can, like, a cheat, cheat cheat that I can use to hopefully work there one day? Um, so, the, uh, Typically after this step, it is possibly you'd have another job fit directly with a manager that, you know, you, you know, the feedback from this comes away and it's like our, one of our integrations managers is like, oh, that's a good fit, you know? And so they might interview you for another one that's very similar to this one.

After that, it's typically a, you know, it's a coding test, and it's two and a half hours, but it's pretty open ended. Um, they, they, um, they give you an assignment and tell you, go do it, pick, pick the language you want. Um, and, uh, um, they do typically want you to use AI now.

Do you know if they judge it on completion or on thought process as far as you got? You know that kind of thing? They do weigh pretty heavily, whether you accomplish the requirements or not.

Okay. But, um, using AI, uh, you can, I think the time limit is becoming less and less important as the AI dependency becomes greater because I think, uh, the boilerplate for a lot of these projects is so easy for AI to spit out. Yeah.

So I think, uh, you already, you already have a leg up there. So my suggestion in those is, um, lean on AI for every step of the way, the planning, documentation, have it help you write documentation. As much coding as makes sense, unit tests, try and get a as complete product project as you can. and leverage AI throughout the whole thing.

And, uh, um, uh, that's my advice there. Pick, maybe pick a language that we've talked about or, um, you know, if, uh, you know, if like the integrations engineer, or engineering manager talks to you, they, they're very typescript job script heavy, you know, kind of pick the language that kind of sounds like you're going towards. You don't have to, but it's always nice.

You know, there's, we don't put that much emphasis on, honestly, on particular language skills. Because at a senior level, people have developed the ability to just pick up languages. So, um, there's not that huge of a deal.

And, uh, and after that, it's just, uh, we have other, like, another interview with, uh, more, um, like, director level people, and that's really, um, they'll just tone in on things that the interviewers previously might have marked as, like, hey, we need to look more into this area. Concerns, yes. Yeah.

So anything where there's just question marks of, you know, ability or experience that might be a problem, they might just dig into that a little bit. Yeah, good. I love the opportunity to clear things up versus just being turned away prematurely.

So that's awesome. All right. I see we're over.

Thank you, but you want to say anything before you wrap up? No, thanks a lot for your time. We use that.

I'm sure you saw it, Bright Hire records this transcript of this whole thing and, um, and then, uh, um, I kind of match up questions and answers and things like that with it. So, yeah. And then, um, I'll talk to, uh, our recruiting people and, um, uh, find out what particular positions are remaining and then give them advice on that.

I know we're hiring a lot of positions right now. Yeah, I've heard. That's what the recruiter said on the 1st call, so.

Thank you. All right, cool. thanks a lot. Yeah, bye.

Bye.

---

## Key Takeaways

-   ***

## Follow-up Actions

-
