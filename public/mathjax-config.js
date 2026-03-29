const preamble = `
\\DeclareMathOperator{\\im}{im}
\\DeclareMathOperator{\\ker}{ker}
\\DeclareMathOperator{\\sign}{sign}
\\DeclareMathOperator{\\ccl}{ccl}
\\DeclareMathOperator{\\Re}{Re}
\\DeclareMathOperator{\\Im}{Im}
\\DeclareMathOperator{\\var}{var}
\\DeclareMathOperator{\\cov}{cov}
\\DeclareMathOperator{\\cl}{cl}
\\DeclareMathOperator{\\scl}{scl}
\\DeclareMathOperator{\\tr}{tr}
\\DeclareMathOperator{\\rk}{rk}
\\DeclareMathOperator{\\Sym}{Sym}
\\DeclareMathOperator{\\GL}{GL}
\\DeclareMathOperator{\\SL}{SL}
\\DeclareMathOperator{\\ord}{ord}
\\DeclareMathOperator{\\Log}{Log}
\\DeclareMathOperator{\\Aut}{Aut}
\\DeclareMathOperator{\\Gal}{Gal}
\\DeclareMathOperator{\\Hom}{Hom}
\\DeclareMathOperator*{\\Res}{Res}
\\DeclareMathOperator*{\\limup}{\\,{\\uparrow} lim\\,}
\\DeclareMathOperator*{\\limdown}{\\,{\\downarrow} lim\\,}

\\newcommand{\\id}{\\mathrm{id}}
\\newcommand{\\op}{\\operatorname}
\\newcommand{\\R}{\\mathbb{R}}
\\newcommand{\\C}{\\mathbb{C}}
\\newcommand{\\Z}{\\mathbb{Z}}
\\newcommand{\\Q}{\\mathbb{Q}}
\\newcommand{\\N}{\\mathbb{N}}
\\newcommand{\\I}{\\mathrm{I}}
\\newcommand{\\II}{\\mathrm{II}}
\\newcommand{\\se}{\\{#1\\}}
\\newcommand{\\sb}[2]{\\left\\{#1\\;\\middle|\\; #2\\right\\}}
\\newcommand{\\actson}{\\curvearrowright}
\\newcommand{\\mrm}[1]{\\mathrm{#1}}
\\newcommand{\\Ci}{\\mathbb{C}_\\infty}
\\newcommand{\\inv}{^{-1}}
\\newcommand{\\pmat}[1]{\\begin{pmatrix}#1\\end{pmatrix}}
\\newcommand{\\gen}[1]{\\left\\langle #1 \\right\\rangle}
\\newcommand{\\isom}{\\cong}
\\newcommand{\\v}[1]{\\boldsymbol{\\mathbf{#1}}}
\\newcommand{\\vhat}[1]{\\hat{\\v{#1}}}
\\newcommand{\\dv}[1]{\\dot{\\v{#1}}}
\\newcommand{\\ddv}[1]{\\ddot{\\v{#1}}}
\\newcommand{\\matr}[1]{\\mathsf{#1}}
\\newcommand{\\ub}{\\underbrace}
\\newcommand{\\union}{\\cup}
\\newcommand{\\inter}{\\cap}
\\newcommand{\\sumi}[3]{\\sum_{{#1} = {#2}}^{#3}}
\\newcommand{\\sl}[2]{\\mathrm{SL}_{#1}(#2)}
\\newcommand{\\gl}[2]{\\mathrm{GL}_{#1}(#2)}
\\newcommand{\\prob}{\\operatorname{\\mathbb{P}}}
\\newcommand{\\expect}{\\operatorname{\\mathbb{E}}}
\\newcommand{\\d}{\\operatorname{d\\!}{}}
\\newcommand{\\dfd}[3][]{\\frac{\\mathrm{d}^{#1}{#2}}{\\mathrm{d}{#3}^{#1}}}
\\newcommand{\\dvd}[3][]{\\frac{\\mathrm{d}^{#1}\\v{#2}}{\\mathrm{d}{#3}^{#1}}}
\\newcommand{\\pdfd}[3][]{\\frac{\\partial^{#1}{#2}}{\\partial{#3}^{#1}}}
\\newcommand{\\pdvd}[3][]{\\frac{\\partial^{#1}\\v{#2}}{\\partial{#3}^{#1}}}
\\newcommand{\\dd}[2][]{\\frac{\\mathrm{d}^{#1}}{\\mathrm{d}{#2}^{#1}}}
\\newcommand{\\pdd}[2][]{\\frac{\\partial^{#1}}{\\partial{#2}^{#1}}}
\\newcommand{\\pdxd}[2]{\\frac{\\partial^2}{\\partial{#1}\\partial{#2}}}
\\newcommand{\\pdfxd}[3]{\\frac{\\partial^2{#1}}{\\partial{#2}\\partial{#3}}}
\\newcommand{\\vnabla}{\\v\\nabla}
\\newcommand{\\mathbsf}[1]{\\boldsymbol{\\mathsf{#1}}}
\\newcommand{\\ouline}[1]{\\overline{\\underline{#1}}}
\\newcommand{\\tto}{\\rightrightarrows}

\\newcommand{\\for}[5][=]{#2_{{#3}{#1}{#4}}^{#5}}
\\newcommand{\\fsum}[4][=]{\\for[#1]{\\sum}{#2}{#3}{#4}}

\\newcommand{\\operp}{⦹}

\\newcommand{\\rel}{\\ \\ \\mathrm{rel}\\ }

\\newcommand{\\mapsfrom}{\\leftarrow\\!\\shortmid}

`

MathJax = {
    tex: {
        inlineMath: [['$', '$']],
        displayMath: [['$$', '$$']],
    },
    startup: {
        ready: () => {
            MathJax.startup.defaultReady();
            MathJax.tex2chtml(preamble);

            const unicodeRanges = MathJax._.core.MmlTree.OperatorDictionary.RANGES;
            unicodeRanges[4][0] = 0x03AC;
            unicodeRanges.splice(4, 0, [880, 940, 0, "mo"]);
        },
    },
};
