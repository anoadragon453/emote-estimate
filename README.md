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
emowoji-6.json: Emotes: 260, Bytes: 36452, Bytes / Emotes: 140.20
ksp-discord.json: Emotes: 79, Bytes: 12067, Bytes / Emotes: 152.75
emowoji-5.json: Emotes: 260, Bytes: 36452, Bytes / Emotes: 140.20
emowoji-2.json: Emotes: 375, Bytes: 52125, Bytes / Emotes: 139.00
free-software.json: Emotes: 31, Bytes: 6235, Bytes / Emotes: 201.13
yuru-camp.json: Emotes: 89, Bytes: 18186, Bytes / Emotes: 204.34
emowoji-9.json: Emotes: 376, Bytes: 52171, Bytes / Emotes: 138.75
blobhaj.json: Emotes: 66, Bytes: 8746, Bytes / Emotes: 132.52
ksp-forum.json: Emotes: 21, Bytes: 4168, Bytes / Emotes: 198.48
racoon-camp.json: Emotes: 12, Bytes: 3394, Bytes / Emotes: 282.83
emowoji-7.json: Emotes: 375, Bytes: 52162, Bytes / Emotes: 139.10
emowoji-10.json: Emotes: 376, Bytes: 52161, Bytes / Emotes: 138.73
emowoji-4.json: Emotes: 83, Bytes: 12668, Bytes / Emotes: 152.63
emowoji-8.json: Emotes: 375, Bytes: 52162, Bytes / Emotes: 139.10
emowoji-1.json: Emotes: 376, Bytes: 52181, Bytes / Emotes: 138.78
emowoji-3.json: Emotes: 374, Bytes: 52164, Bytes / Emotes: 139.48

Average bytes / emote: 161.12
Max count in pack data: 376
Max emotes that can fit in 65536 bytes: 406
```

Meaning that ~406 emotes could fit into a single state event (image pack).

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
