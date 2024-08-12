# Estimate Emotes

A simple script to estimate the maximum number of
[MSC2545](https://github.com/matrix-org/matrix-spec-proposals/pull/2545) emotes
that can fit into a single state event.

This data was used to determine whether the [current event
size](https://spec.matrix.org/v1.11/client-server-api/#size-limits) (65535
bytes) is a limiting factor in real-world scenarios.

## Results

The initial results of running this repo returned the following data:

```
➜ ./venv/bin/python ./estimate-emotes.py
emowoji-6.json: Emotes: 260, Bytes: 36429, Bytes / Emotes: 140.11
ksp-discord.json: Emotes: 79, Bytes: 12044, Bytes / Emotes: 152.46
emowoji-5.json: Emotes: 260, Bytes: 36429, Bytes / Emotes: 140.11
emowoji-2.json: Emotes: 375, Bytes: 52102, Bytes / Emotes: 138.94
free-software.json: Emotes: 31, Bytes: 6212, Bytes / Emotes: 200.39
yuru-camp.json: Emotes: 89, Bytes: 18163, Bytes / Emotes: 204.08
emowoji-9.json: Emotes: 376, Bytes: 52148, Bytes / Emotes: 138.69
blobhaj.json: Emotes: 66, Bytes: 8723, Bytes / Emotes: 132.17
ksp-forum.json: Emotes: 21, Bytes: 4145, Bytes / Emotes: 197.38
racoon-camp.json: Emotes: 12, Bytes: 3371, Bytes / Emotes: 280.92
emowoji-7.json: Emotes: 375, Bytes: 52139, Bytes / Emotes: 139.04
emowoji-10.json: Emotes: 376, Bytes: 52138, Bytes / Emotes: 138.66
emowoji-4.json: Emotes: 83, Bytes: 12645, Bytes / Emotes: 152.35
emowoji-8.json: Emotes: 375, Bytes: 52139, Bytes / Emotes: 139.04
emowoji-1.json: Emotes: 376, Bytes: 52158, Bytes / Emotes: 138.72
emowoji-3.json: Emotes: 374, Bytes: 52141, Bytes / Emotes: 139.41

Average bytes / emote: 160.78
Max count in pack data: 376
Max emotes that can fit in 65536 bytes: 407
```

Meaning that ~407 emotes could fit into a single state event (image pack).

---

Note that the number of packs in this repository is quite small. However, the
point is to just get a rough estimate and even only a few packs should be
sufficient.

## Methodology

The maximum number of images that can fit in a single pack is calculated as follows:

```
For each image pack:
    Count the number of emotes in the pack;
    Canonicalise the pack JSON and count the bytes;
    Canonicalise the JSON added to an event during federation and add that the pack byte count;

Then, take the average emotes / pack byte count across all packs, and divide
65535 (the maximum federation event byte size) by that count. You'll end up
with a rough estimate for the amount of emoji you can fit in an image pack
when contained within a single state event.
```

## Emote credits

Emote state event JSON was originally taken from public Spaces listed under
[#stickers-and-emojis:tastytea.de](https://matrix.to/#/#stickers-and-emojis:tastytea.de).
