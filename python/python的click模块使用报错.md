# python的click模块使用报错
报错如下:
```
/Users/yuyanchuan/.pyenv/versions/3.4.2/bin/python /Users/yuyanchuan/PycharmProjects/ecm-stateserver/manage.py run_worker
Traceback (most recent call last):
  File "/Users/yuyanchuan/PycharmProjects/ecm-stateserver/manage.py", line 23, in <module>
    cli()
  File "/Users/yuyanchuan/.pyenv/versions/3.4.2/lib/python3.4/site-packages/click/core.py", line 716, in __call__
    return self.main(*args, **kwargs)
  File "/Users/yuyanchuan/.pyenv/versions/3.4.2/lib/python3.4/site-packages/click/core.py", line 675, in main
    _verify_python3_env()
  File "/Users/yuyanchuan/.pyenv/versions/3.4.2/lib/python3.4/site-packages/click/_unicodefun.py", line 119, in _verify_python3_env
    'mitigation steps.' + extra)
RuntimeError: Click will abort further execution because Python 3 was configured to use ASCII as encoding for the environment.  Either run this under Python 2 or consult http://click.pocoo.org/python3/ for mitigation steps.

This system lists a couple of UTF-8 supporting locales that
you can pick from.  The following suitable locales where
discovered: af_ZA.UTF-8, am_ET.UTF-8, be_BY.UTF-8, bg_BG.UTF-8, ca_ES.UTF-8, cs_CZ.UTF-8, da_DK.UTF-8, de_AT.UTF-8, de_CH.UTF-8, de_DE.UTF-8, el_GR.UTF-8, en_AU.UTF-8, en_CA.UTF-8, en_GB.UTF-8, en_IE.UTF-8, en_NZ.UTF-8, en_US.UTF-8, es_ES.UTF-8, et_EE.UTF-8, eu_ES.UTF-8, fi_FI.UTF-8, fr_BE.UTF-8, fr_CA.UTF-8, fr_CH.UTF-8, fr_FR.UTF-8, he_IL.UTF-8, hr_HR.UTF-8, hu_HU.UTF-8, hy_AM.UTF-8, is_IS.UTF-8, it_CH.UTF-8, it_IT.UTF-8, ja_JP.UTF-8, kk_KZ.UTF-8, ko_KR.UTF-8, lt_LT.UTF-8, nl_BE.UTF-8, nl_NL.UTF-8, no_NO.UTF-8, pl_PL.UTF-8, pt_BR.UTF-8, pt_PT.UTF-8, ro_RO.UTF-8, ru_RU.UTF-8, sk_SK.UTF-8, sl_SI.UTF-8, sr_YU.UTF-8, sv_SE.UTF-8, tr_TR.UTF-8, uk_UA.UTF-8, zh_CN.UTF-8, zh_HK.UTF-8, zh_TW.UTF-8

Process finished with exit code 1

```
## 解决办法
1.shell下执行代码，英文环境
```
$ export LC_ALL="en_US.UTF-8"
$ export LANG="en_US.UTF-8"
```
2.ide里面写入环境变量，中文环境
如pycharm里面
```
Environment variables:LC_ALL=zh_CN.UTF-;LANG=zh_CN.UTF-8
```
`注：后面编码格式请在错误信息里面查找使用，如笔者所用zh_CN.UTF-8,区分大小写。`