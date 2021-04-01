import datetime
import calendar
import traceback
from django.contrib.auth.decorators import login_required
import os
from base64 import urlsafe_b64encode
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, InvalidToken
from django.shortcuts import render
from django.http import HttpResponse

from sellapp.models import License, Machine
"""
TODO:
Encrypt functions
Create EXE
Update exe on site
"""


def get_key(password, salt):
    password = password.encode()
    salt = salt.encode()

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())
    return urlsafe_b64encode(kdf.derive(password))


def encrypt(message, fernet):
    if isinstance(message, str):
        message = message.encode()

    return fernet.encrypt(message)


def decrypt(data, fernet):
    return fernet.decrypt(data).decode()


def generate_private_keys():
    private_creds = os.environ.get(
        'private_creds', "(('2.4', private_password, private_salt),)")
    private_creds = eval(private_creds)

    private_fernets = {}
    for version, password, salt in private_creds:
        key = get_key(password, salt)
        fernet = Fernet(key)

        private_fernets[version] = fernet

    return private_fernets


private_password = """?aD2rx5m@hO|3X%l"G2I$qV/9w3.!!kH&x~cirr9Ne20|6@G&l8"?vCs@B30>2^4%n%)P#nu20!c>,6Sj~f,)KN1m@Jnj,,39t>1>Mb?FOl(Z(W1X3wOC,K3|#sIRL^Upc*siOo13"K`L~1LBrmcvkwBr9i6%DS">2(Zk5RsRkoV(ev9YLH>msUe#ocIHVNwDN2`79c)z$H%N)Epus!3CLT68."elOs816c<V$Upyl!T(/95!nuE^?!INGj<2WBC8Y0Q|cv)?)<E``>(mphW/UUjCE.*4bfxO/Y7|>^>"/Wx~tm*9FNP|RvaAxz0D7?,t00iXfyFL/eFvOCju!~Uge7(P~HKUitq/hOnb/3P%C,JZovx$|k2#VSAFWxHoP7F*Oz15%Pw"rLinEf@b/s<b!o5DXq|1yc@F~0O`qHVDi?`w7VR*SlCJqC#~Y0)E9tEXK/i8epW`ms,E/zzc@ehm.?tYYS*UoJe7&yoLxxDC/>Vl/SIkH!^1z%FN,%wgvO?d%%F<ms7.Z!.E*i8c.@g1~AxegDV<.X354QIT@C1mbs!v/PR6i"9%Z"`G/trIFh0vW@zZ06uYY&tQHXU$#tF>GT6RbF3"QCFOU8MxOWkZ!Z(#90bw#K.YSzoDmVY)KlV2)Lv?RVCF!)z>q~k(/6j2RFnZ#Ec1JBAv/`yiXjUTwG"73y>OK6,I$*|3Ww!0e,(1Q9ue7`2gG60xDWYc^iZ<7KH/ZGk$(cUNkHUhr<1w&,dE,I9"d9X&EL1!srp<2sp*&$2L~X7?|OL~G@.*"rX|z#)CPz/kuFjHZUozq(Qo1qRWud@g9Ais.gw)y*6C7lXkQY.#$G?pdxIIrNMW4l,cH*ev>!1Z9cKE?Vttb0TPOVAGK"oTK?(H93*$Pwh"~?$0`/PPp9I%SWD2(Ut!>T/AMTt7,hGvif|zkC.>efKK*Dk.a%43IzD#piml6PDT4^HoLVt"HqZYI~^SzL`.P%IqvW@tw<RjImMnK9C|M,VlG&v*&AA`a%pPl8d4Hm@T6W><c)"V|z7$($AfnXRe4<*@!)&5mCBaUc7<PlgiDA6"JrLLXDOTHS8R$Lh95~hfiIkP"(vML?B>|JCIx.nUUF`tvuYYM34lyA^7<c4z^^!,WEclK&&"#92!qX%2I$KHEdQe4pZW*RtVJ#Gu|uGpMj<6`^Vc<Kx@s|h@2,W994Y*XXdhcO@FK9c$O&KgSWi<~O6Ms<e!GFp,x3Jc%WUdyaK5Zi7qmaf9KlgW>"JImpqpsQb.v"<|QXNLQL/)a@|m`Kw2J,ltdFB>9JB?6B|y<2B)%a@n&pw^eHl.sr,fr4m~kNTY>%/cj4P6xmalCYZ|8Y<P4~f?Zn"SdJ7>qbIP1/kmFW?/L$?"FW.fUr"(!C/Kq<qVGsowIV%MSU*>YNOkR6|vqL`zfo)7folBJhfwsaHI7TC/Uv%mCe|Df#,r@LWG)k9UsnI)&Om/LcdJSw!(?p4jN4?Wj~nk"F^6|eSEm,#T4C4f>ch|YeoceahJ`qMayP"8HOPlJ*2~vVXZi%<dxW9<JC0)TDIN*sEnqlTaK1/9k"8lizcyTB4)RP!7$W34%B9Ijq,&&.)ZgFhmCb`50"dLg.tmoP6)R^4&tR7G@mV,.lZy>C#/Zi(Byl5@F%y?x)6n$?#J<Kr9)p@Jy@GV@u(o?BZpu7|/@R`<Dgah>IqY`D6eMx"nvRbH*kHt.`Qw%@Ca>n!DrV2WGO!CzN4hJyZ(?I<8S$WD~S<wlN##qD>TlK?)Ndl)<bR(8)8YrCF0s^TM60GMD>qxpBqOm(c`1`o6r>?t2ZJ/q&f?rtg>chvb2|*8vN0^,eX.%xKEX6|I<ET.CKfhJZbgde9DOBYKSN(i?CEGKgJhfedESWep~"8VKgPltzeM`drei#ID@ir<`3#(0Q&(`ly3/abW`9/d)g0WqoT&ZAKDze7YiS)PxrF4&(SO@y24j4jOU<1M3v,%|AEgNdi6yt%<sFrIIYV,4D@C$.)B>fVY|$P!UXMkd.xudMM7IFlmZV!nw*C%vT&R/uBfqV,.>PtL>fv,2m`i*Ls"""

private_salt = """@n0n3"TQ>y8AnixKb94M@|qTJ&`gg8uI.gsc1szBo$y$FG@"Sf~vlN!0SzHHq(OqAEZ4)Sl11oO5*kyZMY^5y6HgX!*8QpXq7Mjbw0pz2$|LL*s>!w~l`3`^"Ybz,oK"XV|5xIJ)C$Sao,NA#cGF#aRZk2AWF3JhxUdOlyr*oLj0TQ0)JIhkE#5Y""he)fmA9<UjO/gOl4RU)#r6#$fhGH#i6)J9$/s,4Kav//@GoE3^/vhc0s^>//3Opgr)m?!SjFNa^l"fc>qBz&VxaWA#k~h7#".h4x<Tj,0W|*!C.3mKVa0cS9vm(W&NFDf*rIp`QT.!uE.4PJQ^Fo1hw((2dvzvHkNlR.iY1efQiF.&*FZFiZoS^BehAc(W~BdOLd@@Nz0en0$/ovCpg.(r32<o8d&Ko0M"w`Vq4&zqf9J&#^h97T@3Whx`!~N480l|R|xg1bXSQCZ,FbvO)sN)xLvnJisi`h|D~3`>p3qv.6Husc<hTFL9(UGTLFkX$,2(gU90QSOvxF4ntRK/4k%BGK7"9wnuMq53fV5)bUg?!9ylxp%$*Xzsu4FV?%<LxXcBnOx9AiFLP#M!t$>B>sp@oBgeArddmDE(mMu(Paes)e8H&k3)8MBF^d@d5Nj@x/ESh@bx(Pe(<9<x"po2kj`zM&G8Hxky$g#w(3@/OhM$s(I1!3$2sz@F,Cx2kU1sr$"AMsmUR)pOeEIC.BqpFz62XNw<q@T!Id!g!!1FF44XE1fcGeU0JOLw<hl3Bbz&L&UJd!0SxwgwHAQITvg93a#6~c8NV/k7^NZ5?>e5XYKW.Tt^C^j%veaA%Gc#/zKBdN4ACf^y.ak>8^r*p/U!^Bn&VDbdmx/^VSc5&)ebQ(G%$yn>*hgA6`1m!M6*~A|j7.OS&qWk.A1yS<V`Vb|slf>rJseduecbtcjjfu*R!htTA>q#i!@f|He2^jY1##BRx04kEXv6myUfz&sM>ky&eQM^h#6Q%JHx5.QLWY7Epqicks1oYyre^~vb#i&JKk#>1Ef28.tet1uHqDk8DZ8ExMDN,F.dElBZdVcR#LQVqDl*lUTd2Iq@O4M`vgl<fiAmkNXT`Syna~Wl`"2iPnhhr<C*8Bi#<Y>t3kLvAku(AoW.SIS9Xs*I^0Jaro`2@(orqoI)@WT6ls1ATF2tgrmq2,8^KnJ"8C,`%5D@BI3Sml2D~jWmQaV~fO%K)qu,,X|?Tslv9p.X)9^NpH?|b%,$mtUUwdJ<%W|o,|!/g<rfxP5hCi|jzXh#$#DM`Vt"7SL|"CyMKUy``M$Iq(nW)tc~o3e50iEih6)I>^8?L49YMz<VY`"/McGNM!<N8,Iib$G9H#Iu7)MTow?Z/t`i`Hhl^A(aU$dtLCzo*Bd(L4Uk7C!Vv2f,pfy.XbqN?&sylC7!4uk?oFrGjf7iNQt^TCbf>nUy8~&z@f|)zx6tRUmAmf2UTSw2~20Uvg$^1ssHHdyUR@.C~>y`SrGVrQSnsmOLQafN1po."7LMw&h9))JWp*QxZbKkwC%~NkYMo0drb%cEtb^)JHi&vvqP50cm~CACa2ht3!DXVgmeiXUm3JwRj^UcF1Y6.oc!Ew!iqC)vq0z6D5C)4JB!<RMN,~x$rWzNZ(Ir%g&5j%6C`u)l^QJO6kJ1N0FOwn.l^JswBHSrkRoZu(<GLA3O66df##8U*typ!V`#D4!0@I)x)1QL>GgW(%eDvh7Yu431TXieqdQfcFO/Jk7.wW`IRz4*DC!ULqO#eEs3KXWxA)3K%r24t)LG>JN2T%EU>k.(PTvUUd~X%lMG3%IWm<03eNl`OML^*2!WRWm&E%EMGG6>!$0Mu/mxJ6j1hZmGzX"#eY~OU)F9srJG)glKfZh`@SV@7oD<VkYB>Wi"G3G`(3yX2U"`H#fl&n~^NPjP&EtoA#OX~ou7rCXNcBdiX?63Ot>`%vz&rp`m|rnK3.*/uRihvP">sloGWl9D%JW`UoP!&dp"YQoOBXO^3s>3ca?>VwIk`WF<P8rdgy6c1k?H07aah$J9kNMi.~&Biu#?Slf)F.xxoI21C|3#@a/Dr))9"""

public_password = """5PT&$``P)S$)OoJigmNuBKOI`73>~vZ/)8`wKC>qU7N7T,yzf)5V%%50Ky%hIQimBQc&u/dZ0@/h62.i6xmrHK"Vw"!dP.>XuXxVzRYe#|hdN%#J8N(VTt5z"WPWmW~(RYX^JE`GmiRI$$m>wIZ>aG|Zd#N%"&8Mo"/aBR?#Tx2UqvPTJLM"Am"5G1FFI1@CN8jVKc1aIygc*6I78@2*^5N<YowsY@QZAbco|w|!^5*7DXhjYQ5J3p@>eq6X^siDQBRGeyRgt2OqV5EZS9kkH$#!&,|E!rE8n1ow7d51gbWL?lEdkO)7EZPo>0CNswPHE|ndL&uL9x5o|$r<0ErW5QC2ndvV`#u6.w8?io/^uVE2b(It9@W.`nrz`^L9UAX74)rWiLoP/0.b#Ot%m?cJcY!XRN|p60(aaL.,`S7vL^iF1r!*Ht/v21BB40D^Y6%$"7$RLMl,N)p%X7`)AwYOPyo@?QieTiEobf(Q$95,xa2/Gb~O)R%H%s8D#%#AhQ8TC/Y3vaWGxG,R$1i)jfyl)i)7rKEjaB*&kB19bM7>jKwWoiSbO>JFt`3B|e<5JI#O,y6e1ogx~lCwnB(sA4KTM2<t22a0xBX/Bu5hZm`wv7ipBHwt3oW$v~.hM`N!|k<sAtGrsACP`!.w.Z7WO*3j>~sq6n&1LfwvMU#d$b./On(n"/Sq2p1lwe>Z$wzUFyM0Sxwimm.6RP5c%DY>Y*pARm*~,Z1o$dx?<p>M0Mz",r"&0!MF>ROBP`J!b#s2t~YQcz6OY@t,^m|x<smNN/zc%5sd3QDG8e<jWWel8VuFRZWi@O(ak8U!(wQk#>@WuMxyX%cBJs&PzT^(jpboD3r#ZCB"ZjrslPlm`bpV%k>ql`Tg?H#*Q4a~*HKVZCm)GDw~?mH~4Nbrj~<pZZMIpXji#NksSnpoS5,^/1d,&%7!Oi5id~~0?yxaqp0.olyeRJEHh0<ac|*Cbke9zk~DZyhbj0wg@?DuBlX4"(fT.,QI7w>?e)2n8s5/k6Kw`"<GsJ,DjK!t6zD<V<yxLCPj.k$UcC@C%p`~nK9rNLYrr"Bz*EwvMQ3ZeN5$f,Al*!OWNGvqhn"<~?gUfF^^F3fx1eONGaj!IjfsH8>zI"XCiqGVA@UAd,8)7qMJHj2U%!,6h,7,!pT*i.zD8X0%^uQMH#&%%v9k66f%FIWlGjh2g<K|h$~7iLWnO8!Y$jq`ax3(XnB*pxHsx7/EdpKuvs&IQ#gx7*P2aKHAEN<oWeJL#,o4o3RiCNZ<WOpMUprC4O#kzM<ph?4/GDFH~j$G<*NG#yKubAMraK18nXMdFIlwXD4G/eXh(A*dDrp4gEOb~jkNG%*s8M)pCyl#YPce(q>F?qgPAF"0a^5UEfrMWqS2u"8ZKYtS9EI.ooYh82%XuM$$A^s!7~6z`"gnM~5KYifJFQ5$Mdd/IB<1^crA8GCMXF0oO~>Dhmc!t72^vHS@$w!IHL6QwO!>6lbji7yz)xVRs%USlu"%QDzZhKJOo^KeGAspzm8RA8R^Wr%GOR!Ep<%os<v$o~kYjK@XmoIH6mfr^2NXQ>zpUcFzFH5Zq!fo7UpqS682N/F4JnnR3*>bAq)vbWgowxN8&?6lJ(uSUH$glG"ouY@qL|5m58T0ZxP!m4Pt7|lXffJUSEXa1o#u06WBdanmZSxtvr)e(5wZw#G0d``%yXk5Uq(2o#|vQ*@sZ>"RknG(H^ud>I0AuWS!Mc)H1`ZoDhQ/LF&Hv"qpThDg(Jb1AT5<0$V$p,9ksYVE~glf|^69f70kbgkBf<X<q`OI&xAC)yJ*DK2RdP4K)m^eXW`YW$@VkiG`NVOknfYyn42!AIB6KZo1,67~FomHC%#65ac*xDTS?o2afRcdqA9X`Gta1BCS5^@V`Ome2sjXXq.z?BJ>GUjJYr"sCH7u*wW%&U>ENe5tx|&Nmbnv`0Gk!~HY7FuPom"q1cXw22H$hEuVn7JnpZq2PtmHUTQZ/)o".QR#|76"?k~ZXJC%>LrT4q*Z4l8r*XRqoXZ?90A3/5A%,lgb5WJ"UKYTM)xtRhmNMG7Y"""

public_salt = """T2upK"h1M,WPCY`w&ha6Cl7ZztGnes)lz^V5a?n#k^j~D3h!hiCTEcg~"jtzG#)E,T866y>eB*WrAMVCaT@Je,)ftVpUSvw0juZyl%Vf*lkzcDAM%x3tlP9W)l#$KJ`3)x7!L(5)|u4P%G7V!?14&cP,r`jnl@kR#&g1zbwXeo?"~Kn/etpA0((pks5EjN%?RqMIGNYvZFuKBvpZP&|vsi*J0C#ZqnRCviGEEs1|BeRBveXVWK"nkCHx><$f7WA5w2k%%tOu%^OQ?SjKZ@(%ZLVLr,fB<`RfvQniEy2!3YP%p|jjop$ohTpcxbk,6X&4w)f?WZnhQRg$&/VR2M4iNaM$tuDkXxM^LQvyOf2hxf8#6gqX4^,f2rNuQ5Vrw,>qxa^X@n%v*0T|PVN3j"RXXhhIXIH2oyWd$5%@yi0dxWm)m(sb<&Uf@ibmAacPn?U)DQz3i|FL2&,puE#>kEo(q1x|*|y%s1fd(efJGc5G<t`egWLmJOKm(NDwL%4cYaLjV"P406qB?>,(pvat,8q8v%faP5OR2q3d?<8$j1v"LzyiZ(>4^btdaVGsx0IB3.Dl&.d"KM8#"hJ84pt(&^Q~zT()sNkIRWk?U1jg`5PqXSTaVeFqM#P$SdhUTpt,OCJW$T1GpmJxj!r9lG$7rXipDLC2?fi^.p.0>S8%sxwPp,qrYrySGKVVpK?v1mUwu2En5.zkLu<%U$e8j.di,Fr*CbDgRrAujPj1AJtRo^1((Ts2TcFm2EERj9f~oMbM`tBJFTZNN6HmxbKx(EY9T!QX^C6Ikruq6JRl)rE&DF9vxYC.T6V7Yiq)|qL~x>i/Zfr(KK)7b6mCilR*7PTL@^b)u.J<SS~(uKT`hD,7TdpUkl2k^.ht5CpV,baWP`<5qqW0M3L|ZY1Bq>?DcZ69LSL5*lf9X1p10EzqR|#V&h8Myve?Dwo>DW,h1<zMfS#y9u`MPN!mG(K6&^tjl7?D#cD#/jq^OW*ga|/.n03ejl~W!xs0><^d!0CyI#Gvqyo6OhIB^Eu5,rIeswD$vkiT?1`SyVK~?q&.4^I4aESU%aOgD5$eZEYE4Xc)z?h/*dYlAQ3sFpZLhtQ2V?dA"9$k~/pX,`$gs.uk%wlDX@gEH>HW1|YyqP2i>@JvE^T!$0N5#TQyltE03Y/fUjNe>?"i4T>Av<iFfDoYF`6,KHIl2wCZO)uQ/gxo^K$M^`)3DWykRJZa/>2$PlNWwkmWVr?Fx%&mFOw!^Ql.Db"zMCTh)dt?.E8j>Azx8#uN(Pl0yLiA&/&R)9piJmKqOdUR2OK7983H`l$Z."KcYl6pSP(h#MO?~AoH0G"WQ68QKPD5#^,)LB&oBITplIDetQam(1,%3y(BW<Tog0erd!`b<.Voa%6fBWuu"T|jugV!9^#X!A1vWT.7uX/o^l@I$ptu/kGVAn?L/5(FtM4%n5t~uD`ImTQxsE>byQQE,j^tG.</b17a<p,su4B*lcc"l``!On#Cmr,mE2<MeO"b)q?J>A,w9t9x1IMC*Xi/KN7n*vE3*nPG`wj5c5u2&?kVy8>(Q.N|xeJQT..59h?5%2lG))bfr^4x8Pqf/uo7>guwgP.a`Z8%nQ@C7v`Cztv5@xWkt/uFjd#bvah1Hlm87RY*9|),$n?L@W4<$3iSO`c%J>MI?$YB,0savaM)j?i&)Lsygo4S38y$h(lsfRau"JDl2C&2(BGq%3F"*T^6TAI0fTN)<J,TYKC.HBw9X?gF`7|nqg(2emSW7B1m/&"U.(EbVfh$hq16Q(n?t9JomXYr>g7xpAAR5!FMb9iill&l.y9%mRxe/(ooo<(yUfH2#lW3Dsl(bey(<M<R@oo.OG?De%AcqQ$D#U<~M(QMxK~#G<N?kSFSYM?LD0n2A13F(GKqfk5>eHycPxXY/xYMZ~Vo!oik4iABgf91aqAl`l%,lMpYySd$xWhqR`w6aon&vJ>Wv.72`TNu,ZL@7Mln.B,>%lwIIOG9~4HUEP!6d"2/B<d2!*i?|.K?`^Fl<~489Pt|yicy6#z7<Jmr<OjN`dn&|ue)pYF(ikyJ"""

# public key for decrypting args
public_password = os.environ.get('public_password', public_password)
public_salt = os.environ.get('public_salt', public_salt)
key = get_key(public_password, public_salt)
public_fernet = Fernet(key)

private_fernets = generate_private_keys()


def decrypt_code(version, encrypted_code):
    try:
        fernet = private_fernets.get(version)

        encrypted_code = f'gAAAAAB{encrypted_code}'
        encrypted_code = encrypted_code.encode()
        decrypted_code = decrypt(encrypted_code, fernet)
        return decrypted_code
    except:
        return 'error'


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def is_license_valid(request, args, code_mode=False):
    print()
    print('is_license_valid')

    try:
        args_decrypted = decrypt(args.encode(), public_fernet)
    except InvalidToken:
        return 'error'

    args = args_decrypted.split('/')

    if code_mode:
        username, license_key, bios_sn, csproduct, mac_id, system, version, processor, model, encrypted_code, app_version = args
    else:
        username, license_key, bios_sn, csproduct, mac_id, system, version, processor, model, app_version = args

    try:
        print('license_key', license_key)
        print(License.objects.first().key)

        license = License.objects.get(key=license_key)
        if license.user.username != username:
            print('License username doesnt match')
            return 'License not found, maximum machines limit is reached, or machine is blacklisted by an owner of the license.'

        period = int(license.additional_info)

        if period:
            expiration_date = add_months(license.creation_date, period)
            print('now', datetime.date.today())
            print('expiration_date', expiration_date)
            
            if datetime.date.today() > expiration_date:
                license.delete()
                return 'License expired'

        allowed_machines = license.machine_set.all().filter(
            is_blacklisted=False)

        banned_machines = license.machine_set.all().filter(is_blacklisted=True)

        hardware_id = f'{bios_sn}, {csproduct}, {mac_id}'
        info = f'{system} {version}, {processor}'
        current_machine = None

        print('hardware_id', hardware_id)
        print('info', info)
        print('model', model)

        try:
            print('Trying to find existing machine')
            # If it's existing machine, update last login time
            current_machines = allowed_machines.order_by('-last_login')
            current_machines = allowed_machines.filter(hardware_id=hardware_id,
                                                       model=model,
                                                       info=info)
            current_machine = current_machines.first()
            current_machine.update_last_login_time()

            print('Found machine')
            print('hardware_id', hardware_id)
            print('info', info)
            print('model', model)

        except Exception as e:
            print('No machine found')
            print(e)

            banned_machines = banned_machines.order_by('-last_login')
            banned_machines = banned_machines.filter(hardware_id=hardware_id,
                                                     model=model,
                                                     info=info)
            current_machine = banned_machines.first()
            if current_machine is not None:
                return 'Owner of the license banned this machine.'

        try:
            if current_machine is None:
                print('Creating new machine')
                if len(allowed_machines) < license.max_machines_limit:
                    print('Under limit')
                    new_machine = Machine()
                    new_machine.create_machine(hardware_id, info, model, False,
                                               license)
                current_machine = new_machine

                print('hardware_id', hardware_id)
                print('info', info)
                print('model', model)
                print('Created new machine!')
        except Exception as e:
            print('Too many machines')
            return 'Maximum machines limit reached on this license.'

        if current_machine is not None:
            if code_mode:
                return app_version, encrypted_code

            return 'success'

    except Exception as e:
        print(e)
        traceback.format_exc()
        # except (License.DoesNotExist, Machine.DoesNotExist) as e:

    print('No license found: ERROR')
    return 'License not found, maximum machines limit is reached, or machine is blacklisted by an owner of the license.'


def license_check(request, args):
    os.system('cls')
    print('license_check')

    result = is_license_valid(request, args)
    if result == 'success':
        print('OK!')
        print('\n' * 3)
        return HttpResponse('ok')

    print('Here')
    print(result)
    return HttpResponse(result)


def decrypt_code_with_license(request, args):
    os.system('cls')
    print('decrypt_code_with_license')

    try:
        app_version, encrypted_code = is_license_valid(request,
                                                       args,
                                                       code_mode=True)
        print('Decrypt code')
        decrypted_code = decrypt_code(app_version, encrypted_code)
        print('\n' * 3)

        return HttpResponse(decrypted_code)
    except:
        pass


def render_machines(machines):
    return [(
        machine.id,
        machine.info,
        machine.model,
        machine.last_login,
    ) for machine in machines]


@login_required
def view_machines(request):
    user = request.user
    licenses = user.license_set.all()
    info = []

    for license in licenses:
        key = license.key
        key = f'{key[:8]}{"*" * 15}'

        allowed_machines = license.machine_set.all().filter(
            is_blacklisted=False)
        banned_machines = license.machine_set.all().filter(is_blacklisted=True)

        rendered_allowed_machines = render_machines(allowed_machines)
        rendered_banned_machines = render_machines(banned_machines)

        info.append((key, rendered_allowed_machines, rendered_banned_machines))

    context = {'info': info}
    return render(request, 'main/view_machines.html', context=context)


def ban_machine(request, machine_id):
    user = request.user

    machine = Machine.objects.get(id=machine_id)
    machine_user = machine.license.user

    if machine_user == user:
        machine.is_blacklisted = True
        machine.save()
        return HttpResponse('true')

    return HttpResponse('"Error ocurred. Refresh page and try again, please."')


def unban_machine(request, machine_id):
    user = request.user

    machine = Machine.objects.get(id=machine_id)
    machine_user = machine.license.user

    if machine_user == user:
        user_allowed_machines = machine.license.machine_set.filter(
            is_blacklisted=False)
        if len(user_allowed_machines) < machine.license.max_machines_limit:
            machine.is_blacklisted = False
            machine.save()
            return HttpResponse('true')

        return HttpResponse(
            f'"Maximum machines limit is reached. Current limit: {machine.license.max_machines_limit}"'
        )

    return HttpResponse('"Error ocurred. Refresh page and try again, please."')


"""
Trying to decrypt args

Try to get license

If machine already exists:
    update login time
else: 
    check if account's limit were not reached
    Create a new machine
Decrypt code
"""
