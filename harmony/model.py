# -*- coding: utf-8 -*-


import datetime

from biryani1.strings import slugify
from biryani1.baseconv import check
from biryani1.objectconv import object_to_clean_dict
from suq.monpyjama import Mapper, Wrapper


class Jobs(Mapper, Wrapper):
    collection_name = 'jobs'

    upload_at = None
    filename = None
    status = False
    step = 0

    def save(self, *args, **kwargs):
        if self.upload_at is None:
            self.upload_at = datetime.datetime.utcnow()
        return super(Jobs, self).save(*args, **kwargs)

    def to_bson(self):
        # find a unique slug base on filename
        slug = slugify(self.filename)
        distinguish = 1
        while True:
            proposal = slug if distinguish == 1 else '%s-%d' % (slug, distinguish)
            if not Jobs.find_one({'slug': proposal}):
                slug = proposal
                break
            distinguish += 1
        
        self.slug = slug
        return check(object_to_clean_dict(self))
