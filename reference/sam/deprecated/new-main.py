"""
# summarize plaulist - count artist sonfas - if more than 5 add
# new
# year caches, genres caches

# add 10 libarry songs to saved a day - cycles

#! TODO https://streamlit.io/components - attribute

# ytm syncing
"""

from datetime import datetime
from os import system
from time import sleep
from json import load, dump
from pydash import flatten
import re

from _const import *
from functions import SAM, sp, jprint, mem, TRACK, SAVED, usr
from pocketbase import PocketBase
from pocketbase.client import ClientResponseError

#! does not work on pi - device dependent
with open("meta.json", "r") as f:
    meta = load(f)
pb = PocketBase("http://127.0.0.1:8092", "en-US")

lib = mem.pname("_unsorted")
nost = mem.pname("_nostalgia")


def channelGenres():
    print("channelGenres")
    mem.move(lib["id"], None, mem.sids)
    for g in BASE_GENRES:
        print(g)
        src = mem.pname(g + " Mix")
        src_ids = mem.get_track_ids(src)
        dst = mem.pname(g)
        dst_ids = mem.get_track_ids(dst)
        # mem.move(SAVED, dst["id"], mem.diff(mem.intersect(mem.sids, src_ids), dst_ids))
        mem.move(None, dst["id"], mem.diff(mem.intersect(mem.sids, src_ids), dst_ids))
        #   mem.move(
        #       lib["id"], dst["id"], mem.diff(mem.intersect(mem.sids, src_ids), dst_ids)
        #   )
        #   mem.move(
        #       None, dst["id"], mem.diff(mem.intersect(mem.sids, src_ids), dst_ids)
        #   )
        mem.move(SAVED, None, dst_ids)
        mem.move(lib["id"], None, dst_ids)

    # dup
    for g in [*CHANNELS]:
        dst = mem.pname(g)
        dst_ids = mem.get_track_ids(dst)

        for src in CHANNELS[g]:
            print(src)
            src = mem.pname(src)
            src_ids = mem.get_track_ids(src)

            mem.move(
                None, dst["id"], mem.diff(mem.intersect(mem.sids, src_ids), dst_ids)
            )
            mem.move(SAVED, None, dst_ids)
            mem.move(lib["id"], None, dst_ids)

    print("COMPLETE")

    return


def storeArtists():
    if cur_sid in [*db]:  # record should have been updated
        db[cur_sid] = pb.records.update(
            "spotify",
            db[cur_sid].id,
            {"sid": cur_sid, "playcount": db[cur_sid].playcount + 1, "genres": genres},
        )
    else:
        db[cur_sid] = pb.records.create(
            "spotify", {"sid": cur_sid, "playcount": 1, "genres": genres}
        )
    return


def removeDuplicates():
    return


def moveUnsortedtoSaved():
    # lib_ids = mem.get_track_ids(lib)
    mem.move(lib["id"], SAVED, mem.get_track_ids(lib)[:100])


# daily genre artist
# cycles - remove if removed from liked songs
# new scan in - playlist record for future CHANNELING
# listen queue  - unheard/skip labeling - music preference
# pritatives everything
# cycles
# genres -> subgrene; art-coll, channleling
# remove nostaliga from saved
# new by year
if __name__ == "__main__":
    TEST = False

    #  storeArtists()
    #  storeNewTracks()

    channelGenres()

    if (
        not TEST and datetime.now().strftime("%Y-%m-%d") != meta["lastUnsortedToSaved"]
    ):  # per week 140
        print("Moving songs into saved from _unsorted")
        red = mem.pname("Reduce")
        #  moveUnsortedtoSaved()
        mem.move(lib["id"], red["id"], mem.get_track_ids(lib)[:30])
        meta["lastUnsortedToSaved"] = datetime.now().strftime(
            "%Y-%m-%d"
        )  # , datetime.now())
        with open("meta.json", "w") as f:
            dump(meta, f, indent=2)

        # remove those that are a wekk or two old
        for t in mem.retrieve(TRACK, pid=red["id"]):
            if (
                datetime.now()
                - datetime.strptime(t["added_at"].split("T")[0], "%Y-%m-%d")
            ).days > 14:
                mem.move(red["id"], None, t["track"]["id"])
