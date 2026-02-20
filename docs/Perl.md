# Perl

Other languages:

- English
- [français](Perl_fr.md)

## Description

[Perl](http://www.perl.org) is a free programming language which is interpreted and has acquired a vast library of contributed packages over the 25+ years of its existence. Its strengths are manipulating strings, database access and its portability ([according to this article](http://www.cio.com/article/175450/You_Used_Perl_to_Write_WHAT_)). Its weaknesses are its poor performance and the ease with which one can write obscure and illegible code. By design, Perl offers several different ways of accomplishing the same task. Many programmers have adopted this language and write code that is very compact but difficult to decipher.

## Loading the Interpreter

The Perl language is made available on Compute Canada's servers using a module which you can load like any other, e.g.

```
[name@server ~]$ module spider perl

```

to see which versions are installed and then

```
[name@server ~]$ module load perl/5.36.1

```

to load a particular version.

## Installing Packages

A large number of Perl packages can be installed by means of the [Comprehensive Perl Archive Network](http://www.cpan.org/), by using the tool cpan, which however must first be initialized correctly in order to install them in your home directory.

### Initial Configuration for Package Installation

During the first execution of the command cpan the utility will ask you if you want to allow it to configure the majority of settings automatically. Respond yes.

```
[name@server ~]$ cpan

...

Would you like me to configure as much as possible automatically? [yes]
...
What approach do you want?  (Choose 'local::lib', 'sudo' or 'manual')
 [local::lib] 
...

```

The cpan utility will offer to append a variety of environment variable settings to your .bashrc file, which you should agree to. You can then type the command quit at the interface to exit the cpan software. Before installing any Perl modules you will need to restart your shell for these new settings to take effect.

### Package Installation

When the initial configuration is done, you can install any of the more than 25,000 packages available on CPAN. For example:

```
[name@server ~]$ cpan

Terminal does not support AddHistory.

cpan shell -- CPAN exploration and modules installation (v2.11)
Enter 'h' for help.

cpan[1]> install Chess

...
Running install for module 'Chess'
Fetching with LWP:
http://www.cpan.org/authors/id/B/BJ/BJR/Chess-0.6.2.tar.gz
Fetching with LWP:
http://www.cpan.org/authors/id/B/BJ/BJR/CHECKSUMS
Checksum for /home/stubbsda/.cpan/sources/authors/id/B/BJ/BJR/Chess-0.6.2.tar.gz ok
Scanning cache /home/stubbsda/.cpan/build for sizes
............................................................................DONE
'YAML' not installed, will not store persistent state
Configuring B/BJ/BJR/Chess-0.6.2.tar.gz with Makefile.PL
Checking if your kit is complete...
Looks good
...
Running make for B/BJ/BJR/Chess-0.6.2.tar.gz
...
Running make test
PERL_DL_NONLAZY=1 "/cvmfs/soft.computecanada.ca/nix/store/g8ds64pbnavscf7n754pjlx5cp1mkkv1-perl-5.22.2/bin/perl" "-MExtUtils::Command::MM" "-MTest::Harness" "-e" "undef *Test::Harness::Switches; test_harness(0, 'blib/lib', 'blib/arch')" t/*.t
t/bishop.t ......... ok   
t/board.t .......... ok     
t/checkmate.t ...... ok   
t/game.t ........... ok       
t/king.t ........... ok   
t/knight.t ......... ok     
t/movelist.t ....... ok     
t/movelistentry.t .. ok     
t/pawn.t ........... ok     
t/piece.t .......... ok     
t/queen.t .......... ok   
t/rook.t ........... ok   
t/stalemate.t ...... ok   
All tests successful.
Files=13, Tests=311,  3 wallclock secs ( 0.14 usr  0.05 sys +  2.49 cusr  0.20 csys =  2.88 CPU)
Result: PASS
...
Installing /home/stubbsda/perl5/man/man3/Chess::Piece::Knight.3
Installing /home/stubbsda/perl5/man/man3/Chess.3
Installing /home/stubbsda/perl5/man/man3/Chess::Piece::Bishop.3
Installing /home/stubbsda/perl5/man/man3/Chess::Board.3
Appending installation info to /home/stubbsda/perl5/lib/perl5/x86_64-linux-thread-multi/perllocal.pod
  BJR/Chess-0.6.2.tar.gz
  /cvmfs/soft.computecanada.ca/nix/var/nix/profiles/16.09/bin/make install  -- OK

cpan[2]>

```