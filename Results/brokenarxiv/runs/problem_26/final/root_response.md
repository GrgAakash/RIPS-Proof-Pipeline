Completed the fresh solver-only S0-S6 run with no verifier pipeline, no web, and no code-based solving. The pipeline did **not** prove the statement. S6 found that the statement is false as written.

Counterexample to the claimed “if” direction:

Take two players. Player 1 has
\[
(a,u,v,h,r)\in \mathbb R_+^5,\qquad (z_A,z_B,z_C)\in \mathbb Z_+^3
\]
and player 2 has \(y\in \mathbb R_+\). Let
\[
f_1=-2a-yu+yv-4h,\qquad f_2=0.
\]
Thus \(Q_{11}=Q_{22}=0\); the \(yu,yv\) terms are cross-player terms.

Player 1 constraints:
\[
z_A+z_B+z_C=1,\quad a=z_A,\quad h=z_C,
\]
\[
u\le y,\ u\le 2z_B,\quad v\le y,\ v\le 2z_C,\ v\ge y-2+2z_C,
\]
\[
r\le 2,\ r\le 2-2z_B,\ r\ge 2z_C,
\]
\[
r-y\le 2(1-z_A),\quad y-r\le 2(1-z_A).
\]
Player 2 constraints:
\[
y\le 2,\qquad y=r.
\]
All data are rational and all equalities can be written as pairs of rational linear inequalities.

For fixed \(y\in[0,2]\), player 1’s three integer modes have values
\[
V_A=-2,\qquad V_B=-y^2,\qquad V_C=y^2-4.
\]
Mode \(A\) is optimal exactly when \(y^2=2\); mode \(B\) is better when \(y^2>2\), and mode \(C\) is better when \(y^2<2\). Player 2’s constraint forces \(y=r\).

So there is a Nash equilibrium at
\[
z_A=1,\ z_B=z_C=0,\ a=1,\ u=v=h=0,\ r=y=\sqrt2.
\]
Every equilibrium must have \(y=r=\sqrt2\), hence no equilibrium is rational.

So even with \(Q_{ii}=0\) for all players, a rational-data MI-LQ-GNEP can have equilibria but no rational equilibrium. The requested theorem cannot be proved without additional hypotheses.