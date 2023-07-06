#!/usr/bin/perl
=encoding utf8
=head1 LICENSE

Copyright (C) 2022  Petr Písař L<mailto:ppisar@redhat.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

=cut

use utf8;
use strict;
use warnings;
use Test::More tests => 13;
use File::Temp ();
use Cwd ();

sub save_file {
	my ($name, $content) = @_;
	open(my $fh, '>', $name) or die "Could not create $name file: $!";
	$fh->print($content);
	close($fh) or die "Could not save $name: $!";
	return 1;
}
sub read_file {
	my ($name) = @_;
	open(my $fh, '<:encoding(UTF-8)', $name) or die "Could not open $name file: $!";
    local $/ = undef;
	my $content = $fh->getline();
	close($fh) or die "Could not read $name: $!";
	return $content;
}

my $tmp_dir = File::Temp->newdir();
ok($tmp_dir, 'Temporary directory created');
my $old_cwd = Cwd::cwd();
ok($old_cwd, 'A working directory obtained');
ok(chdir($tmp_dir), 'Change a working directory to the temporary directory');


ok(save_file('test.tex',<<'SOURCE'), 'TeX source created');
\documentclass{article}
\usepackage[backend=biber]{biblatex}
\addbibresource{a.bib}
\begin{document}
Hello~\cite{foobar2022}.

\printbibliography
\end{document}
SOURCE
ok(save_file('a.bib', <<'SOURCE'), 'BibTex source created');
@article{foobar2022,
        author   = {Foo and Bar},
        title    = {The paper},
        journal  = {The journal},
        date     = {2022},
        keywords = {trusted},
}
SOURCE

ok(!system('pdflatex', 'test.tex'), 'Run pdflatex to extract a bibliography');
ok(!system('biber', 'test.bcf'), 'Run biber to process the bibliography');
ok(!system('pdflatex', 'test.tex'), 'Run pdflatex to compute a page layout');
ok(!system('pdflatex', 'test.tex'), 'Run pdflatex to insert the references');

ok(!system('pdftotext', '-nopgbrk', 'test.pdf'), 'Convert PDF to plain text');

my $typeset_text = read_file('test.txt');
ok($typeset_text, 'plain text read');

is($typeset_text, <<'EXPECTED', 'Bibliography typeset correctly');
Hello [1].

References
[1]

Foo and Bar. “The paper”. In: The journal (2022).

1

EXPECTED

ok(chdir($old_cwd), 'Change a workking directory back to the original directory');
