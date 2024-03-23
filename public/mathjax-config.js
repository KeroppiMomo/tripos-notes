const preamble = `
\\DeclareMathOperator{\\im}{im}
\\DeclareMathOperator{\\ker}{ker}
\\DeclareMathOperator{\\sign}{sign}
\\DeclareMathOperator{\\ccl}{ccl}
\\DeclareMathOperator{\\Re}{Re}
\\DeclareMathOperator{\\Im}{Im}
\\DeclareMathOperator{\\var}{var}
\\DeclareMathOperator{\\cov}{cov}
\\newcommand{\\op}{\\operatorname}
\\newcommand{\\R}{\\mathbb{R}}
\\newcommand{\\C}{\\mathbb{C}}
\\newcommand{\\Z}{\\mathbb{Z}}
\\newcommand{\\Q}{\\mathbb{Q}}
\\newcommand{\\N}{\\mathbb{N}}
\\newcommand{\\se}[1]{\\{#1\\}}
\\newcommand{\\sb}[2]{\\{#1\\mid #2\\}}
\\newcommand{\\actson}{\\curvearrowright}
\\newcommand{\\mrm}[1]{\\mathrm{#1}}
\\newcommand{\\Ci}{\\mathbb{C}_\\infty}
\\newcommand{\\inv}{^{-1}}
\\newcommand{\\pmat}[1]{\\begin{pmatrix}#1\\end{pmatrix}}
\\newcommand{\\gen}[1]{\\left\\langle #1 \\right\\rangle}
\\newcommand{\\isom}{\\cong}
\\newcommand{\\v}[1]{\\mathbf{#1}}
\\newcommand{\\vhat}[1]{\\hat{\\v{#1}}}
\\newcommand{\\dv}[1]{\\dot{\\v{#1}}}
\\newcommand{\\ddv}[1]{\\ddot{\\v{#1}}}
\\newcommand{\\ub}{\\underbrace}
\\newcommand{\\union}{\\cup}
\\newcommand{\\inter}{\\cap}
\\newcommand{\\sumi}[3]{\\sum_{{#1} = {#2}}^{#3}}
\\newcommand{\\sl}[2]{\\mathrm{SL}_{#1}(#2)}
\\newcommand{\\gl}[2]{\\mathrm{GL}_{#1}(#2)}
\\newcommand{\\prob}{\\operatorname{\\mathbb{P}}}
\\newcommand{\\expect}{\\operatorname{\\mathbb{E}}}
\\newcommand{\\dfd}[3][]{\\frac{\\mathrm{d}^{#1}{#2}}{\\mathrm{d}{#3}^{#1}}}
\\newcommand{\\dvd}[3][]{\\frac{\\mathrm{d}^{#1}\\v{#2}}{\\mathrm{d}{#3}^{#1}}}
\\newcommand{\\pdfd}[3][]{\\frac{\\partial^{#1}{#2}}{\\partial{#3}^{#1}}}
\\newcommand{\\pdvd}[3][]{\\frac{\\partial^{#1}\\v{#2}}{\\partial{#3}^{#1}}}
\\newcommand{\\dd}[2][]{\\frac{\\mathrm{d}^{#1}}{\\mathrm{d}{#2}^{#1}}}
\\newcommand{\\pdd}[2][]{\\frac{\\partial^{#1}}{\\partial{#2}^{#1}}}
\\newcommand{\\vnabla}{\\v\\nabla}

\\newcommand{\\for}[5][=]{#2_{{#3}{#1}{#4}}^{#5}}
\\newcommand{\\fsum}[4][=]{\\for[#1]{\\sum}{#2}{#3}{#4}}
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
        },
    },
};
