#Discord library
import discord
from discord.ext import commands

#Utiliatry
import random
import itertools
import asyncio
from src.command_names import CommandFields

#Imports from other files
from src.youtube import *

async def sendMessage(ctx: commands.Context, *messages,**f) :
    for msg in messages :
        await ctx.send(msg.format(**f))

async def addReaction(ctx: commands.Context, *reactions) :
    for reac in reactions :
        await ctx.message.add_reaction(reac)

async def cmdEffect(ctx,cmd: CommandFields,**details) :
    void = ["",[],[""]]
    if cmd.msg   not in void :
        if type(cmd.msg) == list :
            await sendMessage(ctx, *cmd.msg,**details)
        else :
            await sendMessage(ctx, cmd.msg,**details)
    if cmd.emoji not in void :
        await addReaction(ctx, *cmd.emoji)

class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(
                                   self),
                               color=discord.Color.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    """A class that manages song queues, extends the queue class from asyncio
    """
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        """Gets the length of the queue

        Returns:
            int: The size
        """
        return self.qsize()

    def clear(self):
        """Clears the queue
        """
        self._queue.clear()

    def shuffle(self):
        """Shuffles the queue
        """
        random.shuffle(self._queue)

    def remove(self, index: int):
        """Removes an element at the given index

        Args:
            index (int): The index of the item to be removed
        """
        del self._queue[index]