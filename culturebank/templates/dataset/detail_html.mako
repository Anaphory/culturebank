<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

<<<<<<< aeb701f068041ea28d385d757cafa1adf2cf110c
<h2>Welcome to GramSunDa</h2>

<p class="lead">
GramSunDa is a database of structural (typological) features of languages of the Lesser Sunda Islands.
It consists of more than 200 logically independent features (most of them binary) spanning all subdomains of morphosyntax.
The GramSunDa feature questionnaire has been expanded from <a href="http://glottobank.org/?grambank">GramBank</a> an been filled in, based on reference grammars and active field work, for about 20 languages and varieties in the region.
</p>

<p>
GramSunDa is produced by a team directed by Marian Klamer, as part of a VICI project at Leiden University Centre for Linguistics.</p>

<p>
The original questionnaire was designed by Ger Reesink and
=======
<h2>Welcome to CultureBank</h2>

<p class="lead">
CultureBank is a database of structural (typological) features of language. It consists of 200 logically independent features (most of them binary) spanning all subdomains of morphosyntax. The CultureBank feature questionnaire has been filled in, based on reference grammars, for over 500 languages. The aim to eventually reach as many as 3,500 languages. The database can be used to investigate deep language prehistory, the geographical-distribution of features, language universals and the functional interaction of structural features.
</p>

<p>
CultureBank produced by a team directed by Russell Gray and Quentin
Atkinson. The original questionnaire was designed by Ger Reesink and
>>>>>>> Rename this grambank fork to culturebank III
Michael Dunn, subsequent extensions and clarifications were done by
Hedvig Skirg&aring;rd, Suzanne van der Meer, Harald Hammarstr&ouml;m,
Stephen Levinson, Hannah Haynie, Jeremy Collins, Nicholas Evans, and Hanna Fricke.</p>

<p>
<table class="table table-condensed table-nonfluid">
    <thead>
    <tr>
        <th colspan="3">Statistics</th>
    </tr>
    </thead>
    <tbody>
    <tr><td>Languages</td><td></td><td>${stats['language']}</td></tr>
    <tr><td>Features</td><td></td><td>${stats['parameter']}</td></tr>
    <tr><td>Datapoints</td><td></td><td></td></tr>
    % for name, count in contribs:
        <tr><td></td><td>${name}</td><td>${count}</td></tr>
    % endfor
     <tr><td></td><td><b>total</b></td><td>${stats['value']}</td></tr>
    </tbody>
</table>
</p>

<h3>How to use CultureBank</h3>
<p>
Using CultureBank requires a browser with Javascript enabled.
</p>
<p>
You find the features or languages of CultureBank through the items "Features" and "Languages" in the navigation bar.
</p>


<p>
CultureBank is a publication of the
<a href="http://www.vici.marianklamer.org/">NWO Vici Grant Research Project (2014-2019) “Reconstructing the past through languages of the present: the Lesser Sunda Islands”</a> at the ${h.external_link('https://www.universiteitleiden.nl/en/humanities/leiden-university-centre-for-linguistics', label='Leiden University Centre for Linguistics')}.
</p>

<h3>How to cite CultureBank Online</h3>
<p>
</p>

<h3>Terms of use</h3>
<p>
The content of this web site is published.
We invite the community of users to think about further applications for the available data
and look forward to your comments, feedback and questions.
</p>
