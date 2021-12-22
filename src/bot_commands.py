from discord.ext import commands
import math

#Imports from other files
from src.youtube import *
from src.voice import *

help_str = """**List of the commands : **
Commands syntax is `!command`, i.e. `!play`
*Voice channel : *
\t -`join`
\t Makes the bot join
\t -`leave`
\t Makes the bot leave

*Control :*
\t -`play [source]`
\t Plays the song
\t -`pause`
\t Pause the song
\t -`resume`
\t Resume the song
\t -`loop`
\t Makes a loop with the current song (1 song)
\t -`stop`
\t Stops all
\t -`skip`
\t Skip the current song to the next
\t -`shuffle` (shuffles the playlist)
\t Shuffles the playlist
\t -`remove [inded]`
\t Removes the song at the given index

*Info :*
\t -`now`
\t Displays the current song
\t -`queue`
\t Displays the queue
\t -`aled`
\t Displays this message

*Other :*
\t -`volume [v]` ( 0 <= v <= 100) 
\t Sets the volume of the bot
"""

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

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.send('Sup\' bitches, I\'m in {}'.format(destination))
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon')
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        """Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError(
                'You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='leave', aliases=['disconnect', 'die', 'fix'])
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        await ctx.message.add_reaction('👋')
        del self.voice_states[ctx.guild.id]

    @commands.command(name='volume')
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if not(0 <= volume <= 100):
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_state.volume = volume / 100
        await ctx.send('Volume of the player set to {}%'.format(volume))

    @commands.command(name='now', aliases=['current', 'playing'])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause', aliases=['stop', 'zawarudo'])
    @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')
            await ctx.send('ZA WARUDO !! TOKI WO TOMARE !!')

    @commands.command(name='resume', aliases=['continue'])
    @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')
            await ctx.send('Toki wa ugoki dasu.')

    @commands.command(name='clear')
    @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')
            await ctx.send('Kirā kuīn wa sudeni kyū ni sawatte iru')

    @commands.command(name='skip', aliases=['next'])
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            return

        voter = ctx.message.author
        if voter.guild_permissions.administrator or voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            await ctx.message.add_reaction('😧')
            await ctx.send('Jikan wa futtobashita')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)
            min_votes = (len(ctx.voice_client.channel.members) - 1) // 2 + 1

            if total_votes >= min_votes:
                await ctx.message.add_reaction('⏭')
                await ctx.message.add_reaction('😧')
                ctx.voice_state.skip()
            else:
                await ctx.send('Skip vote added, currently at **{}/{}**'.format(total_votes, min_votes))

        else:
            await ctx.send('You have already voted to skip this song.')

    @commands.command(name='queue', aliases=['list'])
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
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(
                i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(name='shuffle')
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('🔀')

    @commands.command(name='remove')
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('❌')

    @commands.command(name='loop')
    async def _loop(self, ctx: commands.Context):
        """Loops the currently playing song.
        Invoke this command again to unloop the song.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('🔁')
        await ctx.send('Kore ga... Requiem... da.')

    @commands.command(name='play')
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
                await ctx.send('Enqueued {}'.format(str(source)))

    @commands.command(name='aled')
    async def _help(self, ctx: commands.Context):
        """
        List of the commands
        """
        return await ctx.send(help_str)

    @commands.command(name='bedwars', aliases=['bedowaru', 'hypixel', 'BW', 'Bedwars', 'BedWars', 'bw'])
    @commands.has_permissions(manage_guild=True)
    async def _bedwars(self, ctx: commands.Context):
        """
        Pings the @G@m3r role in the #general channel with a random line,
        in order to make them join the server and play BedWars.
        """
        ligne = random.choice(['ramenez votre cul, on fait des bedwars',
                                'c\'est l\'heure des bedwars',
                                'go bedowaru',
                                'venez on fait un bedwars',
                                'on part sur Hypixel'])
        general_channel = self.bot.get_channel(690524800799735848)
        await general_channel.send('<@&860190155973459989> ' + ligne)


    @commands.command(name='ping', aliases=['Ping'])
    async def _help(self, ctx: commands.Context):
        """
        Answers "Pong!" to ping.
        """
        return await ctx.send("Pong!")

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError(
                'You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel and not ctx.author.guild_permissions.administrator:
                raise commands.CommandError(
                    'Bot is already in a voice channel.')
