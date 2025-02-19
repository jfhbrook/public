#!/usr/bin/env perl

use v5.40;
use utf8;
use warnings;

use Data::Dumper;
use Getopt::Long;
use List::Util 'any';
use XML::Parser;

package main;

my $HELP =
'Usage: dbus-iface-markdown [--help] [--system | --session | --bus=ADDRESS | --peer=ADDRESS] [--sender=NAME] [--dest=NAME] [--reply-timeout=MSEC] <PATH>

PARAMETERS:
  PATH  An optional object path (defaults to /)

OPTIONS:
  --help                Show this help message
  --bus ADDRESS         Connect to the bus at the supplied address
  --dest DEST           Dbus destination
  --out FILE            File to write output to (defaults to stdout)
  --peer ADDRESS        Connect to the peer bus at the supplied address
  --reply-timeout MSEC  Set a reply timeout
  --sender SENDER       Dbus sender
  --session             Connect to the session bus
  --system              Connect to the system bus
';

my $help        = '';
my $bus_address = '';
my $dest;
my $out_file      = '';
my $out           = \*STDOUT;
my $peer_address  = '';
my $reply_timeout = -1;
my $sender        = '';
my $session       = '';
my $system        = '';

GetOptions(
    "help"            => \$help,
    "bus=s"           => \$bus_address,
    "dest=s"          => \$dest,
    "out=s"           => \$out_file,
    "peer=s"          => \$peer_address,
    "reply-timeout=i" => \$reply_timeout,
    "sender=s"        => \$sender,
    "session"         => \$session,
    "system"          => \$system
) or die($HELP);

my $object_path = "/";

if ( $#ARGV > 0 ) {
    $object_path = shift(@ARGV);
}

if ($help) {
    print $HELP;
    exit 0;
}

if ($out_file) {
    open( $out, '>', $out_file ) or die("Can not write to $out_file $!");
}

my $send_args = '';

if ($bus_address) {
    $send_args .= "--bus=$bus_address ";
}

if ($peer_address) {
    $send_args .= "--peer=$peer_address ";
}

if ($system) {
    $send_args .= '--system ';
}

if ($session) {
    $send_args .= '--session ';
}

if ($sender) {
    $send_args .= "--sender=$sender ";
}

if ( $reply_timeout > 0 ) {
    $send_args .= "--reply-timeout=$reply_timeout ";
}

my $res = `dbus-send $send_args \\
  --dest=$dest '$object_path' \\
  --print-reply \\
  org.freedesktop.DBus.Introspectable.Introspect`;

my $doc = &response($res);

&visit_node( @{ $doc->[1] } );

close $out;

sub response {
    my ($raw) = @_;
    $raw =~ s/\"$//;

    my @res = split /\n/, $raw;
    @res = splice @res, 3;

    my $doc    = join "\n", @res;
    my $parser = XML::Parser->new( Style => 'Tree' );
    $parser->parse($doc);
}

sub visit_node {
    print $out "# $dest ($object_path)\n\n";
    while (@_) {
        my $child = shift;
        if ( $child eq 'interface' ) {
            my $iface = shift;
            &visit_iface( @{$iface} );
        }
    }
}

sub visit_iface {
    my %props = %{ shift @_ };

    if ( $props{'name'} =~ /^org.freedesktop/ ) {
        return;
    }
    print $out "## Interface: $props{'name'}\n\n";
    while (@_) {
        my $child = shift;
        if ( $child eq 0 ) {
            shift;
            next;
        }
        elsif ( $child eq 'method' ) {
            &visit_method( @{ shift @_ } );
        }
        elsif ( $child eq 'property' ) {
            &visit_property( @{ shift @_ } );
        }
        elsif ( $child eq 'signal' ) {
            &visit_signal( @{ shift @_ } );
        }
        else {
            &dump($child);
        }
    }
}

sub visit_method {
    my %props = %{ shift @_ };
    print $out "### Method: $props{'name'}\n\n";
    my @args;
    my $ret = 'void';
    my @anns;

    while (@_) {
        my $child = shift;
        if ( $child eq 0 ) {
            shift;
            next;
        }
        elsif ( $child eq 'arg' ) {
            my @children = @{ shift @_ };
            my %props    = %{ $children[0] };
            if ( $props{'direction'} eq 'in' ) {
                push( @args, $props{'type'} );
            }
            elsif ( $props{'direction'} eq 'out' ) {
                $ret = $props{'type'};
            }
            else {
                &dump($child);
            }
        }
        elsif ( $child eq 'annotation' ) {
            my $ann = &visit_annotation( @{ shift @_ } );
            push @anns, $ann;
        }
        else {
            &dump($child);
        }
    }

    if (@args) {
        print $out '**Arguments:** ';
        print $out join( ", ", map { "`$_`" } @args ) . "\n";
        print $out "\n";
    }
    print $out "**Returns:** `$ret`\n\n";

    print_annotations(@anns);
}

sub visit_property {
    my %props = %{ shift @_ };
    print $out "### Property: $props{'name'}\n\n";
    my $type   = $props{'type'};
    my $access = $props{'access'};
    my @anns;

    print $out "**Type:** `$type`\n\n";
    print $out "**Access:** `$access`\n";

    while (@_) {
        my $child = shift;
        if ( $child eq 0 ) {
            shift;
            next;
        }
        elsif ( $child eq 'annotation' ) {
            my $ann = &visit_annotation( @{ shift @_ } );
            push @anns, $ann;
        }
        else {
            &dump($child);
        }
    }

    if (@anns) {
        print $out "\n";
    }

    print_annotations(@anns);
}

sub visit_signal {
    my %props = %{ shift @_ };
    print $out "### Signal: $props{'name'}\n\n";
    my $type = 'void';
    my @anns;

    while (@_) {
        my $child = shift;
        if ( $child eq 0 ) {
            shift;
            next;
        }
        elsif ( $child eq 'arg' ) {
            my @children = @{ shift @_ };
            my %props    = %{ $children[0] };
            $type = $props{'type'};
        }
        elsif ( $child eq 'annotation' ) {
            my $ann = &visit_annotation( @{ shift @_ } );
            push @anns, $ann;
        }
        else {
            &dump($child);
        }
    }

    print $out "**Type**: `$type`\n\n";
    print_annotations(@anns);
}

sub visit_annotation {
    my %props = %{ shift @_ };
    "- $props{'name'}: `$props{'value'}`";
}

sub print_annotations {
    if ( !@_ ) {
        return;
    }

    print $out "**Annotations:**\n\n";
    foreach (@_) {
        print $out "$_\n";
    }
    print $out "\n";
}

sub dump {
    my $obj = shift;

    print $out "\n```\n";
    print $out Dumper($obj);
    print $out "```\n\n";
}
