from discord.ext import commands
import math
#Mainly for debug
import tracemalloc
#Imports from other files
from src.youtube import *
from src.voice import *

from src.command_names import *
tracemalloc.start()
class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state
        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage(
                'This command can\'t be used in DM channels.')
        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('An error occurred: {}'.format(str(error)))

    #########################
    ### Join
    @commands.command(**JOIN.args, invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins the voice channel of the person typing the command."""
        
        chan = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(chan)
            return

        await cmdEffect(ctx, JOIN, destination=chan)
        ctx.voice_state.voice = await chan.connect()

    #########################
    ### Leave
    @commands.command(**LEAVE.args)
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        await cmdEffect(ctx, LEAVE)
        del self.voice_states[ctx.guild.id]

    #########################
    ### Volume
    @commands.command(**VOLUME.args)
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if not(0 <= volume <= 100):
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_state.volume = volume / 100
        await cmdEffect(ctx, VOLUME,volume=volume)

    #########################
    ### Now
    @commands.command(**NOW.args)
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())
        await cmdEffect(ctx, NOW)
        
    #########################
    ### Pause
    @commands.command(**PAUSE.args)
    @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await cmdEffect(ctx, PAUSE)

    #########################
    ### Resume
    @commands.command(**RESUME.args)
    @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await cmdEffect(ctx, RESUME)

    #########################
    ### Clear
    @commands.command(**CLEAR.args)
    @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await cmdEffect(ctx, CLEAR)

    #########################
    ### Skip
    @commands.command(**SKIP.args)
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            return

        voter = ctx.message.author
        if voter.guild_permissions.administrator or voter == ctx.voice_state.current.requester:
            await ctx.send("Skipped directly, fuck democracy")
        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes < 3:
                return await ctx.send(f'Skip vote added, currently at **{total_votes}/3**')
        else:
            return await ctx.send('You have already voted to skip this song.')

        await cmdEffect(ctx, SKIP)
        ctx.voice_state.skip()

    #########################
    ### Queue
    @commands.command(**QUEUE.args)
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        """

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += f"`{i+1}.` [**{song.source.title}**]({song.source.url})\n"

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    #########################
    ### Shuffle
    @commands.command(**SHUFFLE.args)
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await cmdEffect(ctx, SHUFFLE)
        
    #########################
    ### Remove
    @commands.command(**REMOVE.args)
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await cmdEffect(ctx, REMOVE)

    #########################
    ### Loop
    @commands.command(**LOOP.args)
    async def _loop(self, ctx: commands.Context):
        """Loops the currently playing song.
        Invoke this command again to unloop the song.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await cmdEffect(ctx, LOOP)

    #########################
    ### Play
    @commands.command(**PLAY.args)
    async def _play(self, ctx: commands.Context, *, search: str):
        """Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await cmdEffect(ctx, PLAY,source=str(source))
                
    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel and not ctx.author.guild_permissions.administrator:
                raise commands.CommandError('Bot is already in a voice channel.')