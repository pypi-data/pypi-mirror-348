# Les champs de pistes: an unbounded distributed collaborative music

## Motivations

How could an unlimited number of people collaborate on one piece of music?

How could this be accessible to as many people as possible? To people with little money
or technical knowledge or bandwidth?

How could this happen with as little technology as possible? With no technology?

## The image

Back in the day, all audio was recorded onto magnetic tape. One tape could have multiple
recordings on it, all laid out precisely as 2 or 4 or even 24 thin and perfectly
parallel tracks on a great long tape.

But what if you had unlimited tracks? It wouldn't look like a tape anymore, but a great
field, an unbounced field of independent tracks.

## The champ de pistes

A **champ de pistes** is a conceptual audio tape recorder, with an unbounded number of
tracks called **pistes**, numbered 1, 2, 3, potentially off to infinity.

A group of people start a champ de pistes and agree how to work. They put segments
on pistes, and create mixes for all to hear.

## The details

### Segments

Pistes contain audio **segments**. A segment is the _address_ of an audio recording. It
identifies a portion of an audio recording somewhere, on or off the internet.

The segment's audio is not stored with the segment or the piste - a segment _points_ to
audio, it does not contain audio.

What a "recording" is, is left under-specified. The exact definition of what a recording
is depends on the rules for the specific champ.

The idea of _address_ is also under-specified: there will be technology for things like
URLs and digital audio, but there's nothing stopping a composer from including an
address that asks someone to come and sit in a specific basement and listen to pipes
dripping.

### Mixes

A **mix** is a set of instructions on how to mix pistes from one or more champs into
single piece of audio. A mix can even be a program in Python or some other programming
language.

For many people, a mix would be some sort of human-readable score they would prepare and
give to someone else's program to prepare the output for them.

That score might also be prepared by a program - for example, a program that reads and
records faders a person uses like a classic mixing board, or something much more
radical.

### About time

A **clip** represents time: it has an optional **début/start time**, and an optional
**durée/duration**.

A _segment_ is just an **address** and a **clip** to the where segment is within the
audio found at the address.

Separately, segments are also **clipped** to a piste - in fact, a piste is nothing
more than a list of segments and clips.

## A concept first, with some technology to make it happen.

I want to re-emphasize that at its base, a champ de pistes is not a technological thing.

A group of people could agree to a champ de pistes and organize it on paper or even in
their heads, creating mixes using stopwatches and whatever devices they had at the time
(LPs, cassettes, MiniDisc, wax cylinders), or even sheet music, singing and a good sense
of time (whether sheet music is a "recording" would depend on what the champ's
definition of a recording was.)

That said, there will be simple free open source software to let you easily make pistes,
champs, and mixes, and and of course listen to them.

## Frequently Anticipated Questions

Q: Champs and pistes: is this a sports thing?

I wanted to emphasize that these aren't conventional tracks at all, and was looking for
a different word. "Field of tracks" in French is "champ de pistes", and I live in
Normandy.


Q: Where is it?

Even though it's purely a conceptual thing, for most people, including myself, some
software will be really what makes it zing.

There will be a workflow involving Git (from any provider, GitLab, GitHub, etc) that
will be automated into a tool to build and share pistes, champs and mixes.

Writing the workflow tool and one simple mixer won't really be a huge amount of time.
Libraries like numpy, requests, and bs4 will do the heavy lifting and I've done an
enormous amount of this stuff before.

In this case, my old proverb really holds - weeks of programming can save you days of
planning.  I intend to get the planning justso before I wrote more than tiny sketches.


Q: Why not just have mixes which include segments, wouldn't that be simpler?
Why have champs and pistes at all?

A: That was my original idea, but it lacked any natural form of collaboration so it sat
in the back of my head for a long time.  Eventually, the idea of the infinite tape
recorder started to crystalize in my head, and then having people work on individual
pistes was the logical next step.


Q: I want to share mixes. What about copyright?

A: I strongly respect copyright laws, and I deplore the fact that composers and
musicians are so poorly compensated.

No copyright material is included in a mix - in fact, no audio material at all, only
addresses. There will be mechanism to turn addresses of, say, Bandcamp or iTunes URLs
tracks that a user has purchased and exist on their machine, into mixes. If you don't
have some track, you get silence, so you could go out and buy the track - or you could
clone the mix and put some other track that you owned in there instead.


Q: Why are the pistes numbered? Why not a name?

You will be able to attach labels to pistes, but any individual piste will always be at
a fixed number like 2, 12 or 23.

Again, this is to thicken the plot: to add a little structure to help collaboration.

You can have pistes that are "right next door" or "far away", or talk about a "block of
pistes".  It adds a geography and a metric to an otherwise trackless world of labels.

More, people can write mixes that work on _any_ champ de pistes, simply by mixing pistes
by index number.

If you want, you can organize your champ so that everything is by label and completely
hide the idea of the piste number, no one is stopping you!
