---
layout: post
title: Beating Google With CouchDB, Celery and Whoosh (Part 8)
date: 2011-10-21 12:00:18.000000000 +01:00
type: post
parent_id: '0'
published: true
password: ''
status: publish
categories:
- web development
tags:
- celery
- celerycrawler
- couchdb
- django
meta:
  _edit_last: '364050'
  _wpas_done_twitter: '1'
  _oembed_5993a6c07def542d7ac1ef4a66578a73: "{{unknown}}"
  _oembed_448e3909cee5fa6959c05c43b00eeac9: "{{unknown}}"
  _oembed_5fdf7ab9d64f0286308ec9b05208f527: "{{unknown}}"
  _oembed_3852527049c1647a35766d00c9ba4473: "{{unknown}}"
  _oembed_d0063f2f78e6d2cdef4e136b54990c30: "{{unknown}}"
  _oembed_319638cd55600eb16edc07d92b73849e: "{{unknown}}"
  _oembed_943a6fff7811ca058cdb2525d5f30f66: "{{unknown}}"
  _oembed_317101bafc70101a89893d181f292bdc: "{{unknown}}"
  _oembed_726fa84ede83630a1429bcbbc14d4f77: "{{unknown}}"
  _oembed_4217b0ebbde63dd25d23021a6b21f166: "{{unknown}}"
  _oembed_c6fb149199f73d4ea3e452c96b6d1c43: "{{unknown}}"
  _oembed_e17d6b446427fd23858ab528e62ad1b4: "{{unknown}}"
  _oembed_6e3a8056be58e9d02de93a4525a65f8c: "{{unknown}}"
  _oembed_531dcd8634e8f155048f976249c72bdb: "{{unknown}}"
  _oembed_ffae00eed36946f8eca5fbe1778732bb: "{{unknown}}"
  _oembed_88b74f680b643070664d7fc69f41e31f: "{{unknown}}"
  _oembed_271d4ab2347f8f0d2aa1547328870b0a: "{{unknown}}"
  _oembed_e4c8f7800c9c61f6f03be81d31ce9c28: "{{unknown}}"
  _oembed_c582b152320b7036d54dcdc34ae90533: "{{unknown}}"
  _oembed_531f0fc468df51708eedadf3ca634347: "{{unknown}}"
  _oembed_4c94bac19a1e4cde67a04474021a8830: "{{unknown}}"
  _oembed_b380acd11a6a8c378e47c3e55cd1d2dc: "{{unknown}}"
  _oembed_2a17c3c823d3b81cd042880a9be69d49: "{{unknown}}"
  _oembed_84d584ae5b0c58f9b4555a14edea5a76: "{{unknown}}"
  _oembed_78147ae1822d2b4cc4d3732e5e130a80: "{{unknown}}"
  _oembed_d9ffdaf7e9f73845a10b3c4a7773204d: "{{unknown}}"
  _oembed_634f515f9600dba4dd8fd97f1f9061b3: "{{unknown}}"
  _oembed_182642deb1f260cf8637901551b11d49: "{{unknown}}"
  _oembed_7557014d6a3aa89954e756f54fa94092: "{{unknown}}"
  _oembed_b1069ffd6c7b758d5fda89ce82d96768: "{{unknown}}"
  _oembed_b15c2448f13ab88b636ac4a61969b74a: "{{unknown}}"
  _oembed_a43d172f22e1041efdc790618c5f7dee: "{{unknown}}"
  _oembed_b9664eeeeaeca2b8a2bf585fba5b41bb: "{{unknown}}"
  _oembed_59a0f01df1f0c833e26c0a1d1d7f5831: "{{unknown}}"
  _oembed_db2f7b632ed20c11f742c815c54f1c17: "{{unknown}}"
  _oembed_79472e0fed21d418e2d4b5de1fafe4bd: "{{unknown}}"
  _oembed_5bd78f2d271d574ff6a0f489cccc676f: "{{unknown}}"
  _oembed_2e94859a58384d6565e7bfd33f671f54: "{{unknown}}"
  _oembed_f20852b73d6987bd6ba04313af54f890: "{{unknown}}"
  _oembed_001885a1e18518e9dfbabbc16c5a5ea5: "{{unknown}}"
  _oembed_63e295a7ba4cfcf69b79564702b951c4: "{{unknown}}"
  _oembed_8029833cb894c640abd0d058e3828cee: "{{unknown}}"
  _oembed_c82449772623a7ae86d2bb35c229e864: "{{unknown}}"
  _oembed_56f25bfb50d529ec8faba7a51b1c0b69: "{{unknown}}"
  _oembed_c0775459c04b1de4969057247a7a962e: "{{unknown}}"
  _oembed_036bafc98df5d3466c319bc0551e4d1b: "{{unknown}}"
  _oembed_705364470b5401412068b9bfbc692d3b: "{{unknown}}"
  _oembed_b8f4707ac64b8d83c7318dc494efad5a: "{{unknown}}"
  _oembed_00567c8907b0a9e7477ab655ea77fa48: "{{unknown}}"
  _oembed_a53d1c58bbeedcca9045e397d839c6ab: "{{unknown}}"
  _oembed_24781da7df4e14491ce8e64d9f6b2555: "{{unknown}}"
  _oembed_2ce1bd7133cc6d2979895dbce0158b2c: "{{unknown}}"
  _oembed_dc7c5310378803796a64c4f3ff82b5a8: "{{unknown}}"
  _oembed_551971e1b8dd46aa2910ad842427ef12: "{{unknown}}"
  _oembed_be1363b362f2ae7416e0526754482d93: "{{unknown}}"
  _oembed_6fff20c2bb040e68b3d632b4b3d094ef: "{{unknown}}"
  _oembed_2a2b1b460df023e7df6325541385a18e: "{{unknown}}"
  _oembed_a20d4751923fa6686b58df424d1fe4c3: "{{unknown}}"
  _oembed_849ab8a7e47a7d18e2eb5af6c8dd1847: "{{unknown}}"
  _oembed_ff0aee8d51780cee871f5e29084d4111: "{{unknown}}"
  _oembed_bdf959269ee2e8b3d700a7a4b95d5db6: "{{unknown}}"
  _oembed_41dd14d1ba088b99648239cc5694779b: "{{unknown}}"
  _oembed_78887389a5b912612ea2f1556838b214: "{{unknown}}"
  _oembed_788932bd68477cc7183b5937c13e9c4b: "{{unknown}}"
  _oembed_1b238c8fe01da461ea303ac75bb0c0af: "{{unknown}}"
  _oembed_849513633934b7a48c5487cdf6402d1e: "{{unknown}}"
  _oembed_f81531b57269a473e59e3ca4c010c7dd: "{{unknown}}"
  _oembed_21e91c108a92edd499059e20e0ee497d: "{{unknown}}"
  _oembed_786c47d3cebdcd4f8f1b8aa2acd70355: "{{unknown}}"
  _oembed_6669f10aa7b240550407aa79658767f7: "{{unknown}}"
  _oembed_8f7b2719f99752aafde734bd2d74db93: "{{unknown}}"
  _oembed_d371545ab64c0729e4a74d16be6d4ece: "{{unknown}}"
  _oembed_1b6bc03cbc3193ff011dafba23c83bd8: "{{unknown}}"
  _oembed_b40cd2ab082720f58e7f984005eaef1a: "{{unknown}}"
  _oembed_d951ed894f640da619c2cfa7112c77d7: "{{unknown}}"
  _oembed_b158b6b96df114ac620e7a30b938c313: "{{unknown}}"
  _oembed_23c53cdc137d470c985afd50ec2ffb82: "{{unknown}}"
  _oembed_2f75e1413606abec929aea2bc7f26df5: "{{unknown}}"
  _oembed_80506352335eeef8ad1ab7317c7696e3: "{{unknown}}"
  _oembed_6d9b383875780f72108ef4285b03398b: "{{unknown}}"
  _oembed_16d614b023da55608fabc4927843dc00: "{{unknown}}"
  _oembed_4491346cfe2f257db746ae747bb376bb: "{{unknown}}"
  _oembed_fd8368cdfe49a597bc48f5e3a0eece28: "{{unknown}}"
  _oembed_87acc03843a17b43666e35d4ea7ff7cd: "{{unknown}}"
  _oembed_7ec09bc40f1a846ce40f97213b0c2b37: "{{unknown}}"
  _oembed_b0d3185582647407c0c860f44c2f0a82: "{{unknown}}"
  _oembed_ae7195bbda5e2ea125bf6e7e90ec76d9: "{{unknown}}"
  _oembed_afc3b8e3fbdd3ca2141f12564c789380: "{{unknown}}"
  _oembed_9c9a4322f994f67844772372ff90ac05: "{{unknown}}"
  _oembed_4dbf35f3b8b526a0c3551c784e155cac: "{{unknown}}"
  _oembed_c517d2237228a6cf5fbf6ddacd935a10: "{{unknown}}"
  _oembed_ffd1b4c6c9294cd68cd08768419a9ef6: "{{unknown}}"
  _oembed_9d8cab6daf6ab360eac9b14ec9429540: "{{unknown}}"
  _oembed_fc9cc74924c659ec8c89d6f90ed403ac: "{{unknown}}"
  _oembed_c13c83c231b1ec230075b55da174539f: "{{unknown}}"
  _oembed_db90764b431b80327c98fc8f8a585d63: "{{unknown}}"
  _oembed_5d7dd7537f4ac25b0764ea3ab4f42122: "{{unknown}}"
  _oembed_7e8f020722ab53439de6efc46f83c98f: "{{unknown}}"
  _oembed_89af63212a20b1ed5dd272b288c9a66e: "{{unknown}}"
  _oembed_6b65ae2cd3bf8b5b59965482a565bbec: "{{unknown}}"
author:
  login: andrewjw
  email: andrewjwilkinson@gmail.com
  display_name: Andrew Wilkinson
  first_name: Andrew
  last_name: Wilkinson
permalink: "/2011/10/21/beating-google-with-couchdb-celery-and-whoosh-part-8/"
---
<a href="http://www.flickr.com/photos/othree/5228608281/"><img style="float:right;border:0;" src="{{ site.baseurl }}/assets/5228608281_2d50d3855c_m.jpg" alt="github 章魚貼紙" /></a>In the previous seven posts I've gone through all the stages in building a search engine. If you want to try and run it for yourself and tweak it to make it even better then you can. I've put the <a href="https://github.com/andrewjw/celery-crawler">code up on GitHub</a>. All I ask is that if you beat Google, you give me a credit somewhere.n
When you've downloaded the code it should prove to be quite simple to get running. First you'll need to edit settings.py. It should work out of the box, but you should change the <tt>USER_AGENT</tt> setting to something unique. You may also want to adjust some of the other settings, such as the database connection or CouchDB urls.n
To set up the CouchDB views type <tt>python manage.py update_couchdb</tt>.n
Next, to run the celery daemon you'll need to type the following two commands:<br />
[code]<br />
python manage.py celeryd -Q retrieve<br />
python manage.py celeryd -Q process<br />
[/code]n
This sets up the daemons to monitor the two queues and process the tasks. As mentioned in a previous post two queues are needed to prevent one set of tasks from swamping the other.n
Next you'll need to run the full text indexer, which can be done with <tt>python manage.py index_update</tt> and then you'll want to run the server using <tt>python manage.py runserver</tt>.n
At this point you should have several process running not doing anything. To kick things off we need to inject one or more urls into the system. You can do this with another management command, <tt>python manage.py start_crawl http://url</tt>. You can run this command as many times as you like to seed your crawler with different pages. It has been my experience that the average page has around 100 links on it so it shouldn't take long before your crawler is scampering off to crawl many more pages that you initially seeded it with.n
So, how well does Celery work with CouchDB as a backend? The answer is that it's a bit mixed. Certainly it makes it very easy to get started as you can just point it at the server and it just works. However, the drawback, and it's a real show stopper, is that the Celery daemon will poll the database looking for new tasks. This polling, as you scale up the number of daemons will quickly bring your server to its knees and prevent it from doing any useful work.n
The disappointing fact is that Celery could watch the <tt>_changes</tt> feed rather than polling. Hopefully this will get fixed in a future version. For now though, for anything other experimental scale installations RabbitMQ is a much better bet.n
Hopefully this series has been useful to you, and please do download the code and experiment with it!n
<hr />
Photo of <a href="http://www.flickr.com/photos/othree/5228608281/">github 章魚貼紙</a> by <a href="http://www.flickr.com/photos/othree/">othree</a>.n
