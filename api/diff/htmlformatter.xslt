<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
    xmlns:diff="http://namespaces.shoobx.com/diff"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <!-- ====== NAMED TEMPLATES FOR DIFF MARKUP ====== -->

    <!-- Template for marking inserted content -->
    <xsl:template name="mark-diff-insert">
        <ins class="diff-insert">
            <xsl:apply-templates/>
        </ins>
    </xsl:template>

    <!-- Template for marking deleted content -->
    <xsl:template name="mark-diff-delete">
        <del class="diff-del">
            <xsl:apply-templates/>
        </del>
    </xsl:template>

    <!-- Template for marking inserted formatting -->
    <xsl:template name="mark-diff-insert-formatting">
        <span class="diff-insert-formatting">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <!-- Template for marking deleted formatting -->
    <xsl:template name="mark-diff-delete-formatting">
        <span class="diff-delete-formatting">
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <!-- ====== DIRECT DIFF ELEMENT HANDLERS ====== -->

    <!-- Handle diff:insert elements (text-only insertions) -->
    <xsl:template match="diff:insert">
        <ins class="diff-insert">
            <xsl:apply-templates/>
        </ins>
    </xsl:template>

    <!-- Handle diff:delete elements (text-only deletions) -->
    <xsl:template match="diff:delete">
        <del class="diff-del">
            <xsl:apply-templates/>
        </del>
    </xsl:template>

    <!-- ====== METADATA ELEMENTS ====== -->

    <xsl:template match="metadaten">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="jurabk">
<!--        <div class="jurabk"><strong>Kurztitel: </strong> <xsl:apply-templates/></div>-->
    </xsl:template>

    <xsl:template match="amtabk">
        <div class="amtabk"><strong>Amtliche Abkürzung: </strong> <xsl:apply-templates/></div>
    </xsl:template>

    <xsl:template match="ausfertigung-datum">
        <div class="ausfertigung-datum"><strong>Ausfertigungsdatum: </strong> <xsl:apply-templates/></div>
    </xsl:template>

    <xsl:template match="enbez">
        <h2 class="enbez">
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:apply-templates/>
            <xsl:if test="../titel">
                <xsl:text> </xsl:text>
                <xsl:value-of select="../titel"/>
            </xsl:if>
        </h2>
    </xsl:template>

    <xsl:template match="gliederungseinheit">
        <div class="gliederung">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="gliederungskennzahl">
        <span class="gliederungskennzahl"><strong><xsl:apply-templates/></strong></span>
    </xsl:template>

    <xsl:template match="gliederungsbez">
        <span class="gliederungsbez"> <xsl:apply-templates/></span>
    </xsl:template>

    <xsl:template match="gliederungstitel">
        <span class="gliederungstitel"> - <xsl:apply-templates/></span>
    </xsl:template>

    <xsl:template match="titel">
        <!-- titel is handled in the enbez template, so we suppress it here -->
    </xsl:template>

    <xsl:template match="fundstelle">
        <div class="fundstelle">
            <strong>Fundstelle: </strong> <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="standangabe">
        <div class="standangabe">
            <strong>Stand: </strong> <xsl:apply-templates/>
        </div>
    </xsl:template>

    <!-- ====== TEXT CONTENT ELEMENTS ====== -->

    <xsl:template match="Content|textdaten|text">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="fussnoten[node()]">
        <div class="footnotes">
            <hr />
            <h3>Fußnoten</h3>
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <!-- ====== STRUCTURAL ELEMENTS ====== -->

    <xsl:template match="TOC">
        <div class="toc">
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="Revision">
        <div class="revision">
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </div>
    </xsl:template>

    <!-- ====== PARAGRAPH AND BLOCK ELEMENTS ====== -->

    <xsl:template match="P">
        <p>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </p>
    </xsl:template>

    <xsl:template match="Title">
        <strong class="title">
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </strong>
    </xsl:template>

    <xsl:template match="Subtitle">
        <strong class="subtitle">
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </strong>
    </xsl:template>

    <xsl:template match="Ident">
        <strong class="ident">
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </strong>
    </xsl:template>

    <!-- ====== INLINE FORMATTING ELEMENTS ====== -->

    <xsl:template match="BR">
        <br/>
    </xsl:template>

    <xsl:template match="B">
        <strong>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </strong>
    </xsl:template>

    <xsl:template match="I">
        <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
        <xsl:call-template name="apply-diff-wrapper"/>
    </xsl:template>

    <xsl:template match="U">
        <u>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </u>
    </xsl:template>

    <xsl:template match="F">
        <span class="font-formatting">
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </span>
    </xsl:template>

    <xsl:template match="SP">
        <span>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </span>
    </xsl:template>

    <xsl:template match="small">
        <small>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </small>
    </xsl:template>

    <xsl:template match="SUP">
        <sup>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </sup>
    </xsl:template>

    <xsl:template match="SUB">
        <sub>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </sub>
    </xsl:template>

    <xsl:template match="FnR">
        <a href="#{@ID}" class="footnote-ref">
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <sup>[<xsl:value-of select="@ID"/>]</sup>
        </a>
    </xsl:template>

    <xsl:template match="NB">
        <span class="nb">
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </span>
    </xsl:template>

    <xsl:template match="noindex">
        <span class="noindex">
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </span>
    </xsl:template>

    <!-- ====== LIST ELEMENTS ====== -->

    <xsl:template match="DL">
        <dl>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </dl>
    </xsl:template>

    <xsl:template match="DT">
        <dt>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </dt>
    </xsl:template>

    <xsl:template match="DD">
        <dd>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </dd>
    </xsl:template>

    <xsl:template match="LA">
        <div class="la">
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </div>
    </xsl:template>

    <!-- ====== TABLE ELEMENTS ====== -->

    <xsl:template match="table">
        <table>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:apply-templates/>
        </table>
    </xsl:template>

    <xsl:template match="tgroup">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="thead">
        <thead>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:apply-templates/>
        </thead>
    </xsl:template>

    <xsl:template match="tbody">
        <tbody>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:apply-templates/>
        </tbody>
    </xsl:template>

    <xsl:template match="tfoot">
        <tfoot>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:apply-templates/>
        </tfoot>
    </xsl:template>

    <xsl:template match="row">
        <tr>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:apply-templates/>
        </tr>
    </xsl:template>

    <xsl:template match="entry">
        <td>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </td>
    </xsl:template>

    <!-- ====== FOOTNOTE ELEMENTS ====== -->

    <xsl:template match="Footnotes">
        <div class="footnotes">
            <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="Footnote">
        <div class="footnote" id="{@ID}">
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <strong>[<xsl:value-of select="@ID"/>]</strong>
            <xsl:text> </xsl:text>
            <xsl:call-template name="apply-diff-wrapper"/>
        </div>
    </xsl:template>

    <!-- ====== SPECIAL ELEMENTS ====== -->

    <xsl:template match="pre">
        <pre>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </pre>
    </xsl:template>

    <xsl:template match="kommentar">
        <div class="kommentar comment-{@typ}">
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </div>
    </xsl:template>

    <xsl:template match="Citation">
        <cite>
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </cite>
    </xsl:template>

    <!-- ====== HELPER TEMPLATE FOR DIFF HANDLING ====== -->

    <!-- Central template to handle diff attributes on any element -->
        <xsl:template name="apply-diff-wrapper">
        <xsl:choose>
            <!-- Only apply diff markup if this element has diff attributes AND no descendant has diff attributes -->
            <xsl:when test="@diff:insert and not(descendant::*[@diff:insert or @diff:delete or @diff:insert-formatting or @diff:delete-formatting])">
                <xsl:call-template name="mark-diff-insert"/>
            </xsl:when>
            <xsl:when test="@diff:delete and not(descendant::*[@diff:insert or @diff:delete or @diff:insert-formatting or @diff:delete-formatting])">
                <xsl:call-template name="mark-diff-delete"/>
            </xsl:when>
            <xsl:when test="@diff:insert-formatting and not(descendant::*[@diff:insert or @diff:delete or @diff:insert-formatting or @diff:delete-formatting])">
                <xsl:call-template name="mark-diff-insert-formatting"/>
            </xsl:when>
            <xsl:when test="@diff:delete-formatting and not(descendant::*[@diff:insert or @diff:delete or @diff:insert-formatting or @diff:delete-formatting])">
                <xsl:call-template name="mark-diff-delete-formatting"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <!-- ====== BOILERPLATE TEMPLATES ====== -->

    <!-- Remove all processing instructions -->
    <xsl:template match="processing-instruction()"/>

    <!-- Identity template for unmatched elements -->
    <xsl:template match="*">
        <xsl:element name="{local-name()}">
            <xsl:copy-of select="@*[not(namespace-uri() = 'http://namespaces.shoobx.com/diff')]"/>
            <xsl:call-template name="apply-diff-wrapper"/>
        </xsl:element>
    </xsl:template>

    <!-- Handle text nodes and attributes -->
    <xsl:template match="text()">
        <xsl:value-of select="."/>
    </xsl:template>

    <!-- Root template -->
    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

</xsl:stylesheet>